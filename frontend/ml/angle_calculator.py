"""
Joint angle calculation utilities.

Angle computation is pure math with no side effects, making it
easy to unit-test independently from any vision or web code.
"""

import numpy as np
from typing import Dict, Optional, Sequence

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
    a_arr = np.asarray(a, dtype=np.float64)
    b_arr = np.asarray(b, dtype=np.float64)
    c_arr = np.asarray(c, dtype=np.float64)

    # Vertex is B. Build rays from B to A and B to C.
    ba = a_arr - b_arr
    bc = c_arr - b_arr

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    eps = 1e-9
    if norm_ba < eps or norm_bc < eps:
        return 0.0

    cosine = float(np.dot(ba, bc) / (norm_ba * norm_bc))
    cosine = float(np.clip(cosine, -1.0, 1.0))

    angle = float(np.degrees(np.arccos(cosine)))
    # Force principal angle to [0, 180] even under floating-point drift.
    return float(np.clip(angle, 0.0, 180.0))


def _safe_angle(a: Optional[Sequence], b: Optional[Sequence], c: Optional[Sequence]) -> Optional[float]:
    if a is None or b is None or c is None:
        return None
    return calculate_angle(a, b, c)


def compute_body_angles(keypoints: PoseKeypoints) -> Dict[str, Optional[float]]:
    """
    Compute the four diagnostic joint angles from a PoseKeypoints object.

    Returns a dict with keys:
        "Shoulder Angle", "Elbow Angle", "Hip Angle", "Knee Angle"
    """
    return {
        "Shoulder Angle": _safe_angle(keypoints.elbow, keypoints.shoulder, keypoints.hip),
        "Elbow Angle": _safe_angle(keypoints.wrist, keypoints.elbow, keypoints.shoulder),
        "Hip Angle": _safe_angle(keypoints.shoulder, keypoints.hip, keypoints.knee),
        "Knee Angle": _safe_angle(keypoints.hip, keypoints.knee, keypoints.ankle),
    }
