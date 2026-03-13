"""
Natural-language pose feedback generation.

Converts evaluator output into student-friendly corrections and tips.
"""

from typing import Dict, List

from .types import JointEvaluation, PoseEvaluation


_REASON_BY_JOINT: Dict[str, str] = {
    "Shoulder Angle": "to improve shoulder alignment and chest opening",
    "Elbow Angle": "to reduce elbow strain and improve arm stability",
    "Hip Angle": "to improve pelvic alignment and posture control",
    "Knee Angle": "to protect the knee joint and improve balance",
}


def _verb_phrase(joint_name: str, direction: str, severity: str) -> str:
    slight = "slightly" if severity in {"minor", "perfect"} else ""

    if joint_name == "Elbow Angle":
        if direction == "increase":
            return f"Straighten your elbow {slight}".strip()
        if direction == "decrease":
            return f"Soften your elbow bend {slight}".strip()

    if joint_name == "Shoulder Angle":
        if direction == "increase":
            return f"Lift and open your chest {slight}".strip()
        if direction == "decrease":
            return f"Relax your shoulders down {slight}".strip()

    if joint_name == "Hip Angle":
        if direction == "increase":
            return f"Lengthen through your spine and hips {slight}".strip()
        if direction == "decrease":
            return f"Hinge a little deeper from your hips {slight}".strip()

    if joint_name == "Knee Angle":
        if direction == "increase":
            return f"Straighten your knee {slight}".strip()
        if direction == "decrease":
            return f"Bend your knee slightly".strip()

    if direction == "increase":
        return "Open the joint angle slightly"
    if direction == "decrease":
        return "Reduce the joint angle slightly"
    return "Maintain this alignment"


def _format_joint_feedback(result: JointEvaluation) -> str:
    if result.severity == "missing":
        return (
            f"{result.joint_name}: landmark not clearly visible. "
            "Use brighter lighting and keep your full body in frame."
        )

    if result.severity == "perfect":
        return (
            f"{result.joint_name}: good alignment. "
            f"Reason: angle is close to target ({result.detected_angle:.1f}°)."
        )

    action = _verb_phrase(result.joint_name, result.direction, result.severity)
    reason = _REASON_BY_JOINT.get(result.joint_name, "to improve pose alignment")
    return (
        f"{result.joint_name}: {action}. "
        f"Reason: {reason} (current {result.detected_angle:.1f}°, "
        f"target {result.reference_angle:.1f}°)."
    )


def build_pose_feedback(evaluation: PoseEvaluation) -> Dict[str, List[str] | int]:
    """Return UI-ready score, corrections, and improvement tips."""
    corrections: List[str] = []
    tips: List[str] = []

    for result in evaluation.joint_results.values():
        message = _format_joint_feedback(result)
        if result.severity in {"minor", "moderate", "major", "missing"}:
            corrections.append(message)

    if not corrections:
        corrections.append("Great work. Your pose is well aligned across measured joints.")

    major_or_missing = [
        r for r in evaluation.joint_results.values()
        if r.severity in {"major", "missing"}
    ]
    moderate = [
        r for r in evaluation.joint_results.values()
        if r.severity == "moderate"
    ]

    if major_or_missing:
        tips.append("Engage your core to stabilize the full posture before deepening the pose.")
        tips.append("Slow down the movement and hold each position for 2-3 breaths.")
    elif moderate:
        tips.append("Focus on smooth breathing to maintain consistent joint alignment.")
        tips.append("Keep shoulders relaxed and neck neutral to avoid compensation.")
    else:
        tips.append("Maintain this form and gradually increase hold duration.")
        tips.append("Use controlled breathing to keep your alignment consistent.")

    return {
        "score": evaluation.score,
        "corrections": corrections,
        "tips": tips,
    }
