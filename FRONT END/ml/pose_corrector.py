"""
Pose correction logic.

Compares detected joint angles against the reference values in
reference_angles.py and generates human-readable feedback strings.

Rule (configurable via angle_tolerance):
  |detected - reference| <= tolerance  → "Looks correct ✓"
  detected < reference - tolerance     → "Increase {joint} by X°"
  detected > reference + tolerance     → "Decrease {joint} by X°"
"""

import logging
from typing import Dict, List

from .reference_angles import REFERENCE_ANGLES

logger = logging.getLogger(__name__)


def generate_corrections(
    detected_angles: Dict[str, float],
    pose_name: str,
    angle_tolerance: float = 5.0,
) -> List[str]:
    """
    Compare detected angles against the reference for pose_name.

    Args:
        detected_angles: Dict of joint_name → measured angle (degrees).
        pose_name:       Lowercase pose name matching REFERENCE_ANGLES keys.
        angle_tolerance: Accepted deviation before reporting a correction.

    Returns:
        List of human-readable correction strings, one per joint.
    """
    reference = REFERENCE_ANGLES.get(pose_name.lower().strip())
    if reference is None:
        logger.warning("No reference data for pose: '%s'", pose_name)
        return [
            f"No reference data found for '{pose_name}'. "
            "Please check the pose name spelling."
        ]

    corrections = []
    for joint, detected in detected_angles.items():
        ref = reference.get(joint)
        if ref is None:
            continue  # Joint not calibrated for this pose — skip silently.

        diff = detected - ref
        if diff < -angle_tolerance:
            corrections.append(
                f"{joint}: increase by {abs(diff):.1f}° "
                f"(detected {detected:.1f}°, target {ref}°)"
            )
        elif diff > angle_tolerance:
            corrections.append(
                f"{joint}: decrease by {diff:.1f}° "
                f"(detected {detected:.1f}°, target {ref}°)"
            )
        else:
            corrections.append(f"{joint}: looks correct ✓  ({detected:.1f}°)")

    return corrections
