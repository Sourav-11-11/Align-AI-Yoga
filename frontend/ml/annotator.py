"""
Image annotation: draws skeleton and angle labels on the pose image.

Separated from pose_detector and pose_corrector so annotation style can
be changed without touching ML logic, and vice versa.
"""

import cv2
import numpy as np
from typing import Dict, Optional

from .types import PoseKeypoints

# ── Visual style constants ────────────────────────────────────────────────────
BONE_COLOUR   = (255, 120, 30)  # Orange-blue skeleton lines
TEXT_COLOUR   = (255, 255, 255) # White angle labels
JOINT_RADIUS  = 7
BONE_THICKNESS = 2
FONT          = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE    = 0.5
FONT_THICKNESS = 2

SEVERITY_COLORS = {
    "perfect": (0, 210, 70),
    "minor": (0, 220, 220),
    "moderate": (0, 220, 220),
    "major": (0, 60, 230),
    "missing": (120, 120, 120),
}

# Which joints to connect with a bone line.
SKELETON = [
    ("shoulder", "elbow"),
    ("elbow", "wrist"),
    ("shoulder", "hip"),
    ("hip", "knee"),
    ("knee", "ankle"),
]

# Which label to draw near which joint.
ANGLE_JOINT_MAP = {
    "Shoulder Angle": "shoulder",
    "Elbow Angle": "elbow",
    "Hip Angle": "hip",
    "Knee Angle": "knee",
}


def annotate_image(
    image_bgr: np.ndarray,
    keypoints: PoseKeypoints,
    angles: Dict[str, Optional[float]],
    joint_severity: Optional[Dict[str, str]] = None,
) -> np.ndarray:
    """
    Return a copy of image_bgr annotated with the skeleton and angle values.

    Args:
        image_bgr:  Original image in BGR colour space (as loaded by OpenCV).
        keypoints:  Detected joint pixel positions.
        angles:     Computed joint angles to display as text labels.

    Returns:
        New BGR image with skeleton overlay.
    """
    out = image_bgr.copy()

    points = {
        "shoulder": tuple(keypoints.shoulder) if keypoints.shoulder else None,
        "elbow": tuple(keypoints.elbow) if keypoints.elbow else None,
        "wrist": tuple(keypoints.wrist) if keypoints.wrist else None,
        "hip": tuple(keypoints.hip) if keypoints.hip else None,
        "knee": tuple(keypoints.knee) if keypoints.knee else None,
        "ankle": tuple(keypoints.ankle) if keypoints.ankle else None,
    }

    # Draw skeleton bones.
    for start, end in SKELETON:
        if points[start] is None or points[end] is None:
            continue
        cv2.line(out, points[start], points[end], BONE_COLOUR, BONE_THICKNESS)

    angle_to_joint = {
        "Shoulder Angle": "shoulder",
        "Elbow Angle": "elbow",
        "Hip Angle": "hip",
        "Knee Angle": "knee",
    }

    # Draw joint dots with quality colors.
    for joint_name, coord in points.items():
        if coord is None:
            continue

        severity = "perfect"
        if joint_severity:
            joint_angle_name = next((a for a, j in angle_to_joint.items() if j == joint_name), None)
            if joint_angle_name:
                severity = joint_severity.get(joint_angle_name, "perfect")

        color = SEVERITY_COLORS.get(severity, SEVERITY_COLORS["perfect"])
        cv2.circle(out, coord, JOINT_RADIUS, color, -1)

    # Draw angle labels (offset slightly so they don't overlap the joint dot).
    for angle_name, joint_name in ANGLE_JOINT_MAP.items():
        angle_val = angles.get(angle_name)
        if angle_val is None or points[joint_name] is None:
            continue
        x, y = points[joint_name]
        label_pos = (x + 10, y - 10)
        cv2.putText(
            out, f"{int(angle_val)}\u00b0",
            label_pos, FONT, FONT_SCALE, TEXT_COLOUR, FONT_THICKNESS,
        )

    return out
