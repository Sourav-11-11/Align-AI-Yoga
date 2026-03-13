"""
Dashboard route: shows session history for the logged-in user.

Key improvement over the original:
  - Images are stored as FILE PATHS in the database, not raw BLOBs.
    Serving large BLOBs via Python is slow; file paths let Nginx/Flask
    serve them as static files directly, which is orders of magnitude faster.
  - Date filtering is done with parameterised queries (preventing SQL injection).
"""

import logging
from flask import Blueprint, jsonify, render_template, request, session
from .auth import login_required
from ..services.chat_service import build_welcome_payload, generate_chat_payload
from ..utils.db import fetchall

logger = logging.getLogger(__name__)
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_email = session["user_email"]

    if request.method == "POST":
        frm_date = request.form.get("frm_date")
        to_date = request.form.get("to_date")
        rows = fetchall(
            """
            SELECT id, user_name, user_email, mood_name, yoga_name,
                   uploaded_image_path, corrected_image_path, feedback, created_at
            FROM yoga_sessions
            WHERE user_email = %s
              AND DATE(created_at) BETWEEN %s AND %s
            ORDER BY created_at DESC
            """,
            (user_email, frm_date, to_date),
        )
    else:
        rows = fetchall(
            """
            SELECT id, user_name, user_email, mood_name, yoga_name,
                   uploaded_image_path, corrected_image_path, feedback, created_at
            FROM yoga_sessions
            WHERE user_email = %s
            ORDER BY created_at DESC
            """,
            (user_email,),
        )

    # Map raw rows to dicts for readability in the template.
    sessions_data = [
        {
            "id": r[0],
            "user_name": r[1],
            "user_email": r[2],
            "mood_name": r[3],
            "yoga_name": r[4],
            "uploaded_img": r[5],    # file path served from /static/saved_images/
            "corrected_img": r[6],   # file path served from /static/saved_images/
            "feedback": r[7],
            "date": r[8],
        }
        for r in rows
    ]

    return render_template("dashboard.html", dashboard_data=sessions_data)


@dashboard_bp.route("/chatbot")
@login_required
def chatbot():
    welcome = build_welcome_payload()
    session["chatbot_state"] = welcome.get("state", {})
    return render_template(
        "chatbot.html",
        welcome_message=welcome["reply"],
        starter_prompts=welcome["suggestions"],
    )


@dashboard_bp.route("/chatbot/message", methods=["POST"])
@login_required
def chatbot_message():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    current_state = session.get("chatbot_state", {})
    chat_payload = generate_chat_payload(message, current_state)
    session["chatbot_state"] = chat_payload.get("state", current_state)
    return jsonify(
        {
            "reply": chat_payload["reply"],
            "suggestions": chat_payload.get("suggestions", []),
        }
    )
