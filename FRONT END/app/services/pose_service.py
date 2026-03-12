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

from typing import Tuple, List, Optional
from flask import current_app

from ml.pose_detector import extract_keypoints
from ml.angle_calculator import compute_body_angles
from ml.pose_corrector import generate_corrections
from ml.annotator import annotate_image

logger = logging.getLogger(__name__)


def analyze_pose(
    image_path: str,
    pose_name: str,
    angle_tolerance: float = 5.0,
) -> Tuple[List[str], Optional[str]]:
    """
    Full analysis pipeline for a single uploaded image.

    Args:
        image_path:      Absolute path to the saved upload.
        pose_name:       Name of the yoga pose (must match a key in REFERENCE_ANGLES).
        angle_tolerance: Degrees within which a joint angle is considered correct.

    Returns:
        (corrections, annotated_filename)
        corrections         -- List of human-readable feedback strings.
        annotated_filename  -- Filename of the annotated image in saved_images/,
                               or None if detection failed.
    """
    # ── Load image wa
    image_bgr = cv2.imread(image_path)
    if image_bgr is None:
        logger.error("Could not read image at: %s", image_path)
        return ["Could not load the uploaded image."], None

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # ── Detect pose keypoints ─────────────────────────────────────────────────
    keypoints = extract_keypoints(image_rgb)
    if keypoints is None:
        return [
            "No body detected in the image. "
            "Please upload a clearer, full-body photo with good lighting."
        ], None

    # ── Calculate joint angles ────────────────────────────────────────────────
    detected_angles = compute_body_angles(keypoints)

    # ── Generate corrections ──────────────────────────────────────────────────
    corrections = generate_corrections(detected_angles, pose_name, angle_tolerance)

    # ── Annotate and save image ───────────────────────────────────────────────
    annotated_bgr = annotate_image(image_bgr, keypoints, detected_angles)

    save_dir = current_app.config["SAVED_IMAGES_DIR"]
    os.makedirs(save_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    annotated_filename = f"annotated_{base_name}.jpg"
    out_path = os.path.join(save_dir, annotated_filename)
    cv2.imwrite(out_path, annotated_bgr)

    logger.info("Pose '%s' analyzed. Corrections: %d", pose_name, len(corrections))
    return corrections, annotated_filename
