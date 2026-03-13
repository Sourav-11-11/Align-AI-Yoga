"""
Pose analysis service.

Orchestrates the full pose-correction pipeline:
  image → keypoint detection → angle calculation → correction generation
  → image annotation → file save

Routes call this single function; they never touch OpenCV or MediaPipe directly.
"""

import os
import logging
import cv2

from typing import Dict, List, Optional, Tuple
from flask import current_app

from ml.pose_detector import extract_keypoints
from ml.angle_calculator import compute_body_angles
from ml.pose_evaluator import evaluate_pose
from ml.pose_feedback import build_pose_feedback
from ml.annotator import annotate_image

logger = logging.getLogger(__name__)


def analyze_pose(
    image_path: str,
    pose_name: str,
    angle_tolerance: float = 5.0,
) -> Tuple[Dict[str, object], Optional[str]]:
    """
    Full analysis pipeline for a single uploaded image.

    Args:
        image_path:      Absolute path to the saved upload.
        pose_name:       Name of the yoga pose (must match a key in REFERENCE_ANGLES).
        angle_tolerance: Degrees within which a joint angle is considered correct.

    Returns:
        (result, annotated_filename)
        result keys: score (int), corrections (list[str]), tips (list[str]).
        annotated_filename  -- Filename of the annotated image in saved_images/,
                               or None if detection failed.
    """
    # ── Load image wa
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        logger.error("Could not read image at: %s", image_path)
        return {
            "score": 0,
            "corrections": ["Could not load the uploaded image."],
            "tips": [],
        }, None

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # ── Detect pose keypoints ─────────────────────────────────────────────────
    keypoints = extract_keypoints(image_rgb)
    if keypoints is None:
        return {
            "score": 0,
            "corrections": [
                "No body detected clearly. Upload a full-body photo with good lighting."
            ],
            "tips": [
                "Keep your full body visible from head to ankle.",
                "Place the camera at hip height and avoid backlight.",
            ],
        }, None

    # ── Calculate joint angles ────────────────────────────────────────────────
    detected_angles = compute_body_angles(keypoints)

    # ── Evaluate + build natural feedback ─────────────────────────────────────
    evaluation = evaluate_pose(detected_angles, pose_name)
    result = build_pose_feedback(evaluation)
    joint_severity = {
        joint_name: joint_result.severity
        for joint_name, joint_result in evaluation.joint_results.items()
    }

    # ── Annotate and save image ───────────────────────────────────────────────
    annotated_bgr = annotate_image(
        image_bgr,
        keypoints,
        detected_angles,
        joint_severity=joint_severity,
    )

    save_dir = current_app.config["SAVED_IMAGES_DIR"]
    os.makedirs(save_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    annotated_filename = f"annotated_{base_name}.jpg"
    out_path = os.path.join(save_dir, annotated_filename)
    cv2.imwrite(out_path, annotated_bgr)

    logger.info(
        "Pose '%s' analyzed. Score=%s, Corrections=%d",
        pose_name,
        result.get("score", 0),
        len(result.get("corrections", [])),
    )
    return result, annotated_filename
