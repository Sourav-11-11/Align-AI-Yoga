"""
Pose keypoint extraction using MediaPipe Pose.

This module selects the body side (left/right) with better landmark
visibility so downstream angle measurements are more stable.
"""

import logging
import numpy as np
from typing import Dict, Optional, Tuple

from mediapipe.solutions import pose

from .types import PoseKeypoints

logger = logging.getLogger(__name__)

# Initialise MediaPipe landmarks enum once at module level (cheap).
_MP_POSE = pose


def extract_keypoints(
    image_rgb: np.ndarray,
    model_complexity: int = 2,
    min_detection_confidence: float = 0.5,
) -> Optional[PoseKeypoints]:
    """
    Run MediaPipe Pose and return six key joint positions from the better side.

    Args:
        image_rgb:               H×W×3 uint8 RGB array (from cv2.cvtColor).
        model_complexity:        0 (fast) / 1 / 2 (most accurate).
        min_detection_confidence Detection threshold [0, 1].

    Returns:
        PoseKeypoints if a body is detected, else None.
    """
    with _MP_POSE.Pose(
        static_image_mode=True,
        model_complexity=model_complexity,
        min_detection_confidence=min_detection_confidence,
    ) as pose:
        results = pose.process(image_rgb)

    if not results.pose_landmarks:
        logger.warning("MediaPipe: no pose landmarks detected.")
        return None

    lm = results.pose_landmarks.landmark
    h, w = image_rgb.shape[:2]

    joint_map = {
        "left": {
            "shoulder": _MP_POSE.PoseLandmark.LEFT_SHOULDER,
            "elbow": _MP_POSE.PoseLandmark.LEFT_ELBOW,
            "wrist": _MP_POSE.PoseLandmark.LEFT_WRIST,
            "hip": _MP_POSE.PoseLandmark.LEFT_HIP,
            "knee": _MP_POSE.PoseLandmark.LEFT_KNEE,
            "ankle": _MP_POSE.PoseLandmark.LEFT_ANKLE,
        },
        "right": {
            "shoulder": _MP_POSE.PoseLandmark.RIGHT_SHOULDER,
            "elbow": _MP_POSE.PoseLandmark.RIGHT_ELBOW,
            "wrist": _MP_POSE.PoseLandmark.RIGHT_WRIST,
            "hip": _MP_POSE.PoseLandmark.RIGHT_HIP,
            "knee": _MP_POSE.PoseLandmark.RIGHT_KNEE,
            "ankle": _MP_POSE.PoseLandmark.RIGHT_ANKLE,
        },
    }

    def _extract_side(side: str) -> Tuple[Dict[str, Optional[list]], Dict[str, float]]:
        side_data: Dict[str, Optional[list]] = {}
        visibility: Dict[str, float] = {}
        for joint, landmark_id in joint_map[side].items():
            landmark = lm[landmark_id]
            vis = float(getattr(landmark, "visibility", 0.0))
            visibility[joint] = vis

            # Keep missing/low-confidence points as None for graceful handling.
            if vis < 0.30:
                side_data[joint] = None
                continue

            px = int(max(0, min(w - 1, landmark.x * w)))
            py = int(max(0, min(h - 1, landmark.y * h)))
            side_data[joint] = [px, py]

        return side_data, visibility

    left_points, left_visibility = _extract_side("left")
    right_points, right_visibility = _extract_side("right")

    left_score = sum(left_visibility.values())
    right_score = sum(right_visibility.values())
    selected_side = "right" if right_score > left_score else "left"
    chosen_points = right_points if selected_side == "right" else left_points
    chosen_visibility = right_visibility if selected_side == "right" else left_visibility

    available_points = sum(
        1
        for j in ("shoulder", "elbow", "wrist", "hip", "knee", "ankle")
        if chosen_points[j] is not None
    )
    if available_points < 4:
        logger.warning("Pose detected but too many landmarks are missing (available=%d).", available_points)
        return None

    return PoseKeypoints(
        shoulder=chosen_points["shoulder"],
        elbow=chosen_points["elbow"],
        wrist=chosen_points["wrist"],
        hip=chosen_points["hip"],
        knee=chosen_points["knee"],
        ankle=chosen_points["ankle"],
        side=selected_side,
        visibility=chosen_visibility,
    )
