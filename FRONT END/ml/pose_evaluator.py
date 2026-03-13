"""
Pose evaluation logic.

Compares measured joint angles against reference values and produces:
- per-joint severity buckets
- actionable direction (increase/decrease/keep)
- overall pose score (0-100)

This module uses the unified thresholds from evaluation_config.py to ensure
consistent scoring between image upload and webcam modes.
"""

from typing import Dict, Optional

from .reference_angles import REFERENCE_ANGLES
from .evaluation_config import get_severity, get_score
from .types import JointEvaluation, PoseEvaluation


def evaluate_pose(
    detected_angles: Dict[str, Optional[float]],
    pose_name: str,
) -> PoseEvaluation:
    """Evaluate detected angles against pose references using unified thresholds."""
    normalized_pose = pose_name.lower().strip()
    reference = REFERENCE_ANGLES.get(normalized_pose)

    if reference is None:
        return PoseEvaluation(
            pose_name=pose_name,
            score=0,
            joint_results={},
            tips=[
                "Pose reference not found. Verify pose name spelling and try again."
            ],
        )

    joint_results: Dict[str, JointEvaluation] = {}
    score_values = []

    for joint_name, target in reference.items():
        measured = detected_angles.get(joint_name)

        if measured is None:
            result = JointEvaluation(
                joint_name=joint_name,
                detected_angle=None,
                reference_angle=float(target),
                difference=None,
                abs_difference=None,
                severity="missing",
                direction="unavailable",
                score=get_score("missing"),
            )
        else:
            diff = float(measured) - float(target)
            abs_diff = abs(diff)
            # Use unified config for severity classification
            severity = get_severity(abs_diff)
            direction = "keep"
            if severity != "perfect":
                direction = "decrease" if diff > 0 else "increase"

            result = JointEvaluation(
                joint_name=joint_name,
                detected_angle=float(measured),
                reference_angle=float(target),
                difference=diff,
                abs_difference=abs_diff,
                severity=severity,
                direction=direction,
                score=get_score(severity),
            )

        joint_results[joint_name] = result
        score_values.append(result.score)

    overall = int(round(sum(score_values) / max(len(score_values), 1)))

    return PoseEvaluation(
        pose_name=pose_name,
        score=max(0, min(100, overall)),
        joint_results=joint_results,
        tips=[],
    )
