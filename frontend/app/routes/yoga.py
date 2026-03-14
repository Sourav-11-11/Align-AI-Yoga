"""
Yoga-flow routes: home, mood selection, pose recommendation, pose correction.

The original app.py mixed ML logic directly into route functions.
Here, routes only handle HTTP concerns (parsing forms, rendering templates).
All ML work is delegated to service functions.
"""

import os
import random
import shutil
import logging

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    current_app,
    url_for,
    jsonify,
)
from werkzeug.utils import secure_filename

from .auth import login_required
from ..services.pose_service import analyze_pose
from ..services.pose_guide_service import get_pose_guides
from ..services.recommendation_service import get_recommender
from ..utils.db import execute
from ml.reference_angles import REFERENCE_ANGLES
from ml.evaluation_config import get_config_dict

logger = logging.getLogger(__name__)
yoga_bp = Blueprint("yoga", __name__)

_BEGINNER_POSES = ["Sukhasana", "Vriksasana", "Adho Mukha Svanasana"]


def _allowed_file(filename: str) -> bool:
    """Check if file extension is allowed for upload.
    
    Args:
        filename: Original filename from upload
        
    Returns:
        True if file extension is in ALLOWED_EXTENSIONS config, False otherwise
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


# ── Home ──────────────────────────────────────────────────────────────────────

@yoga_bp.route("/home")
@login_required
def home():
    """Display home/dashboard page for logged-in users.
    
    Shows welcome message and quick links to yoga sessions.
    """
    logger.info(f"User accessed home: {session.get('user_email')}")
    return render_template("home.html", user_name=session.get("user_name"))


# ── Step 1: Mood selection → Pose recommendation ──────────────────────────────

@yoga_bp.route("/yoga1", methods=["GET", "POST"])
@login_required
def yoga1():
    """Mood-based pose recommendation engine.
    
    GET: Display mood selection interface
    POST: Process mood selection and return personalized pose recommendations
    """
    try:
        recommender = get_recommender()

        if request.method == "POST":
            mood = request.form.get("mood", "").strip()
            if not mood or mood not in recommender.available_moods:
                flash("Please select a valid mood.", "error")
                logger.warning(f"Invalid mood selected: {mood}")
                return redirect(url_for("yoga.yoga1"))

            recommended_poses = recommender.recommend(
                mood, top_n=current_app.config["TOP_POSES"]
            )
            logger.info(f"Recommended {len(recommended_poses)} poses for mood: {mood}")
            
            pose_guides = get_pose_guides(recommended_poses)

            # Copy one reference image per pose into static/img for display
            poses_dir = current_app.config["POSES_DIR"]
            img_dir = os.path.join(current_app.static_folder, "img")
            os.makedirs(img_dir, exist_ok=True)

            recommended_items = []
            for pose in recommended_poses:
                pose_dir = os.path.join(poses_dir, pose)
                if not os.path.isdir(pose_dir):
                    logger.warning("Pose directory not found: %s", pose_dir)
                    continue
                images = [
                    f for f in os.listdir(pose_dir) if _allowed_file(f)
                ]
                if not images:
                    continue
                chosen = random.choice(images)
                shutil.copy(os.path.join(pose_dir, chosen), os.path.join(img_dir, chosen))
                recommended_items.append({
                    "image_url": f"/static/img/{chosen}",
                    "pose_name": pose,
                    "guide": pose_guides[pose],
                })

            return render_template(
                "yoga2.html", items=recommended_items, mood=mood
            )

        # Prep beginner pose cards for the session page
        poses_dir = current_app.config["POSES_DIR"]
        img_dir = os.path.join(current_app.static_folder, "img")
        os.makedirs(img_dir, exist_ok=True)
        beginner_guides = get_pose_guides(_BEGINNER_POSES)
        beginner_items = []
        for pose in _BEGINNER_POSES:
            pose_dir = os.path.join(poses_dir, pose)
            if not os.path.isdir(pose_dir):
                logger.warning("Beginner pose dir not found: %s", pose_dir)
                continue
            images = [f for f in os.listdir(pose_dir) if _allowed_file(f)]
            if not images:
                continue
            chosen = random.choice(images)
            shutil.copy(os.path.join(pose_dir, chosen), os.path.join(img_dir, chosen))
            beginner_items.append({
                "image_url": f"/static/img/{chosen}",
                "pose_name": pose,
                "guide": beginner_guides[pose],
            })

        return render_template(
            "yoga1.html",
            moods=recommender.available_moods,
            beginner_items=beginner_items,
        )
    except Exception as e:
        logger.error(f"Error in yoga1: {str(e)}")
        flash("Error loading yoga session. Please try again.", "error")
        return redirect(url_for("yoga.home"))


# ── Step 2: User uploads pose image → Correction feedback ────────────────────

@yoga_bp.route("/yoga2", methods=["GET", "POST"])
@login_required
def yoga2():
    if request.method == "POST":
        pose_name = request.form.get("pose_name", "").lower().strip()
        mood = request.form.get("mood", "")
        uploaded_file = request.files.get("img")

        if not uploaded_file or uploaded_file.filename == "":
            flash("No file selected. Please upload an image.", "error")
            return redirect(url_for("yoga.yoga1"))

        if not _allowed_file(uploaded_file.filename):
            flash("Invalid file type. Please upload a PNG or JPG image.", "error")
            return redirect(url_for("yoga.yoga1"))

        filename = secure_filename(uploaded_file.filename)
        save_dir = current_app.config["SAVED_IMAGES_DIR"]
        os.makedirs(save_dir, exist_ok=True)
        image_path = os.path.join(save_dir, filename)
        uploaded_file.save(image_path)

        analysis_result, annotated_filename = analyze_pose(
            image_path,
            pose_name,
            angle_tolerance=current_app.config["ANGLE_TOLERANCE"],
        )

        corrections = analysis_result.get("corrections", [])
        pose_score = analysis_result.get("score", 0)
        improvement_tips = analysis_result.get("tips", [])

        # Persist the session to the database so the Dashboard can show history.
        # Store only the filename (not the full path) — images are served as static files.
        feedback_text = "; ".join(corrections) if corrections else ""
        try:
            execute(
                """
                INSERT INTO yoga_sessions
                    (user_name, user_email, mood_name, yoga_name,
                     uploaded_image_path, corrected_image_path, feedback)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    session.get("user_name"),
                    session.get("user_email"),
                    mood,
                    pose_name,
                    filename,                              # uploaded image filename
                    annotated_filename or "",             # annotated image filename
                    feedback_text,
                ),
            )
        except Exception as exc:
            logger.warning("Could not save session to DB: %s", exc)

        return render_template(
            "yoga3.html",
            feedback=corrections,
            pose_score=pose_score,
            tips=improvement_tips,
            image_name=annotated_filename or filename,
            pose_name=pose_name,
            mood=mood,
        )

    return redirect(url_for("yoga.yoga1"))


# ── Direct pose analysis (from navbar) ───────────────────────────────────────

@yoga_bp.route("/analyze", methods=["GET"])
@login_required
def analyze():
    recommender = get_recommender()
    return render_template(
        "analyze.html",
        poses=recommender.available_poses,
        selected_pose=request.args.get("pose", ""),
    )


@yoga_bp.route("/api/pose-reference", methods=["GET"])
@login_required
def pose_reference_api():
    """
    Return reference angles and evaluation configuration for a specific pose.
    
    This endpoint is used by both webcam analysis and image upload modes
    to ensure they apply the same severity thresholds and scoring logic.
    
    Query params:
        pose (required): Pose name (e.g., "adho mukha svanasana")
    
    Returns:
        {
            "pose": string,
            "reference_angles": dict[str, float],
            "angle_tolerance": float,
            "severity_thresholds": {
                "perfect": 5,
                "minor": 10,
                "moderate": 20
            },
            "scoring_weights": {
                "perfect": 100,
                "minor": 85,
                "moderate": 65,
                "major": 35,
                "missing": 0
            }
        }
    """
    pose_name = (request.args.get("pose") or "").strip().lower()
    if not pose_name:
        return jsonify({"error": "Missing 'pose' query parameter."}), 400

    reference = REFERENCE_ANGLES.get(pose_name)
    if reference is None:
        return jsonify({"error": f"No reference found for pose '{pose_name}'."}), 404

    # Get unified evaluation config
    config = get_config_dict()

    return jsonify(
        {
            "pose": pose_name,
            "reference_angles": reference,
            "angle_tolerance": config["angle_tolerance"],
            "severity_thresholds": config["severity_thresholds"],
            "scoring_weights": config["scoring_weights"],
        }
    )
