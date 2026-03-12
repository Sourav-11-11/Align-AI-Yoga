"""
Image annotation: draws skeleton and angle labels on the pose image.

Separated from pose_detector and pose_corrector so annotation style can
be changed without touching ML logic, and vice versa.
"""

import cv2
import numpy as np
from typing import Dict

from .types import PoseKeypoints

# ── Visual style constants ────────────────────────────────────────────────────
JOINT_COLOUR  = (0, 230, 64)    # Bright green dots at joints
BONE_COLOUR   = (255, 120, 30)  # Orange-blue skeleton lines
TEXT_COLOUR   = (255, 255, 255) # White angle labels
JOINT_RADIUS  = 7
BONE_THICKNESS = 2
FONT          = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE    = 0.5
FONT_THICKNESS = 2

# Which joints to connect with a bone line.
SKELETON = [
    ("left_shoulder", "left_elbow"),
    ("left_elbow",    "left_wrist"),
    ("left_shoulder", "left_hip"),
    ("left_hip",      "left_knee"),
    ("left_knee",     "left_ankle"),
]

# Which label to draw near which joint.
ANGLE_JOINT_MAP = {
    "Shoulder Angle": "left_shoulder",
    "Elbow Angle":    "left_elbow",
    "Hip Angle":      "left_hip",
    "Knee Angle":     "left_knee",
}


def annotate_image(
    image_bgr: np.ndarray,
    keypoints: PoseKeypoints,
    angles: Dict[str, float],
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
        "left_shoulder": tuple(keypoints.left_shoulder),
        "left_elbow":    tuple(keypoints.left_elbow),
        "left_wrist":    tuple(keypoints.left_wrist),
        "left_hip":      tuple(keypoints.left_hip),
        "left_knee":     tuple(keypoints.left_knee),
        "left_ankle":    tuple(keypoints.left_ankle),
    }

    # Draw skeleton bones.
    for start, end in SKELETON:
        cv2.line(out, points[start], points[end], BONE_COLOUR, BONE_THICKNESS)

    # Draw joint dots.
    for coord in points.values():
        cv2.circle(out, coord, JOINT_RADIUS, JOINT_COLOUR, -1)

    # Draw angle labels (offset slightly so they don't overlap the joint dot).
    for angle_name, joint_name in ANGLE_JOINT_MAP.items():
        angle_val = angles.get(angle_name)
        if angle_val is None:
            continue
        x, y = points[joint_name]
        label_pos = (x + 10, y - 10)
        cv2.putText(
            out, f"{int(angle_val)}\u00b0",
            label_pos, FONT, FONT_SCALE, TEXT_COLOUR, FONT_THICKNESS,
        )

    return out
