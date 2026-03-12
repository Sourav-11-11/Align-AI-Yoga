"""
Pose keypoint extraction using MediaPipe Pose.

Encapsulates all MediaPipe calls so the rest of the codebase never imports
mediapipe directly. Swapping to a different detector only requires editing
this single file.
"""

import logging
import numpy as np
from typing import Optional

import mediapipe as mp

from .types import PoseKeypoints

logger = logging.getLogger(__name__)

# Initialise MediaPipe landmarks enum once at module level (cheap).
_MP_POSE = mp.solutions.pose


def extract_keypoints(
    image_rgb: np.ndarray,
    model_complexity: int = 2,
    min_detection_confidence: float = 0.5,
) -> Optional[PoseKeypoints]:
    """
    Run MediaPipe Pose on an RGB image and return the six key joint positions.

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

    def pixel(landmark) -> list:
        """Convert normalised [0,1] landmark coords to image pixel coords."""
        return [int(landmark.x * w), int(landmark.y * h)]

    return PoseKeypoints(
        left_shoulder=pixel(lm[_MP_POSE.PoseLandmark.LEFT_SHOULDER]),
        left_elbow=pixel(lm[_MP_POSE.PoseLandmark.LEFT_ELBOW]),
        left_wrist=pixel(lm[_MP_POSE.PoseLandmark.LEFT_WRIST]),
        left_hip=pixel(lm[_MP_POSE.PoseLandmark.LEFT_HIP]),
        left_knee=pixel(lm[_MP_POSE.PoseLandmark.LEFT_KNEE]),
        left_ankle=pixel(lm[_MP_POSE.PoseLandmark.LEFT_ANKLE]),
    )
