"""
Legacy pose correction adapter.

This module keeps the original `generate_corrections` API used by routes/tests,
but internally delegates to the newer evaluator + natural-language feedback
modules.
"""

import logging
from typing import Dict, List, Optional

from .pose_evaluator import evaluate_pose
from .pose_feedback import build_pose_feedback

logger = logging.getLogger(__name__)


def generate_corrections(
    detected_angles: Dict[str, Optional[float]],
    pose_name: str,
    angle_tolerance: float = 5.0,
) -> List[str]:
    """
    Backward-compatible wrapper returning correction strings.

    `angle_tolerance` is retained for API compatibility; severity thresholds
    are now standardized in `pose_evaluator` (perfect/minor/moderate/major).
    """
    evaluation = evaluate_pose(detected_angles, pose_name)
    if not evaluation.joint_results:
        logger.warning("No reference data for pose: '%s'", pose_name)
        return [
            f"No reference data found for '{pose_name}'. "
            "Please check the pose name spelling."
        ]

    feedback = build_pose_feedback(evaluation)
    return feedback["corrections"]
