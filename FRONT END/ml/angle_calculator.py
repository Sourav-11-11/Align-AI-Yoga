"""
Joint angle calculation utilities.

Angle computation is pure math with no side effects, making it
easy to unit-test independently from any vision or web code.
"""

import numpy as np
from typing import Sequence

from .types import PoseKeypoints


def calculate_angle(a: Sequence, b: Sequence, c: Sequence) -> float:
    """
    Return the angle (degrees) at vertex B formed by the ray A→B and C→B.

    Uses the dot-product formula:
        cos(θ) = (BA · BC) / (|BA| × |BC|)

    Args:
        a, b, c:  2-D or 3-D coordinate sequences  (list, tuple, or ndarray).

    Returns:
        Angle in degrees [0, 180].
    """
    a, b, c = np.array(a, dtype=float), np.array(b, dtype=float), np.array(c, dtype=float)
    ba = a - b
    bc = c - b

    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom == 0.0:
        return 0.0  # Degenerate case: two points are identical.

    cosine = np.dot(ba, bc) / denom
    # Clamp to [-1, 1] to guard against floating-point drift before arccos.
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def compute_body_angles(keypoints: PoseKeypoints) -> dict:
    """
    Compute the four diagnostic joint angles from a PoseKeypoints object.

    Returns a dict with keys:
        "Shoulder Angle", "Elbow Angle", "Hip Angle", "Knee Angle"
    """
    return {
        "Shoulder Angle": calculate_angle(
            keypoints.left_elbow, keypoints.left_shoulder, keypoints.left_hip
        ),
        "Elbow Angle": calculate_angle(
            keypoints.left_wrist, keypoints.left_elbow, keypoints.left_shoulder
        ),
        "Hip Angle": calculate_angle(
            keypoints.left_shoulder, keypoints.left_hip, keypoints.left_knee
        ),
        "Knee Angle": calculate_angle(
            keypoints.left_hip, keypoints.left_knee, keypoints.left_ankle
        ),
    }
