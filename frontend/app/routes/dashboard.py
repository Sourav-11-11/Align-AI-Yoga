"""
Dashboard route: shows session history for the logged-in user.

Key improvements:
  - Images stored as FILE PATHS (not BLOBs) for fast static file serving
  - Parameterised queries prevent SQL injection
  - Calculate user statistics (total sessions, accuracy, streak)
  - Support date range filtering for focused viewing
"""

import logging
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template, request, session
from .auth import login_required
from ..services.chat_service import build_welcome_payload, generate_chat_payload
from ..utils.db import fetchall, fetchone

logger = logging.getLogger(__name__)
dashboard_bp = Blueprint("dashboard", __name__)


def _calculate_user_stats(user_email: str) -> dict:
    """Calculate user practice statistics.
    
    Args:
        user_email: User's email address
        
    Returns:
        Dictionary with stats: total_sessions, avg_accuracy, streak_days
    """
    try:
        # Total sessions
        total_result = fetchone(
            "SELECT COUNT(*) FROM yoga_sessions WHERE user_email = %s",
            (user_email,),
        )
        total_sessions = total_result[0] if total_result else 0
        
        # Get all session dates for streak calculation
        dates_result = fetchall(
            """
            SELECT DISTINCT DATE(created_at)
            FROM yoga_sessions
            WHERE user_email = %s
            ORDER BY DATE(created_at) DESC
            """,
            (user_email,),
        )
        
        # Calculate streak (consecutive days)
        streak_days = 0
        if dates_result:
            today = datetime.now().date()
            current_date = datetime.strptime(str(dates_result[0][0]), "%Y-%m-%d").date()
            
            # Allow streak to include today or yesterday
            if (today - current_date).days <= 1:
                streak_days = 1
                for i in range(1, len(dates_result)):
                    prev_date = datetime.strptime(str(dates_result[i][0]), "%Y-%m-%d").date()
                    if (current_date - prev_date).days == 1:
                        streak_days += 1
                        current_date = prev_date
                    else:
                        break
        
        return {
            "total_sessions": total_sessions,
            "streak_days": streak_days,
        }
    except Exception as e:
        logger.error(f"Error calculating user stats: {str(e)}")
        return {"total_sessions": 0, "streak_days": 0}


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Display user dashboard with session history and statistics.
    
    GET: Show all sessions (or filtered by date range if POST)
    POST: Filter sessions by date range
    """
    user_email = session["user_email"]
    user_name = session.get("user_name", "User")
    
    # Get user statistics
    stats = _calculate_user_stats(user_email)
    
    # Fetch sessions (with optional date filtering)
    if request.method == "POST":
        frm_date = request.form.get("frm_date")
        to_date = request.form.get("to_date")
        logger.info(f"Dashboard filter: {user_email} from {frm_date} to {to_date}")
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

    # Map raw rows to dicts for readability in templates
    sessions_data = [
        {
            "id": r[0],
            "user_name": r[1],
            "user_email": r[2],
            "mood_name": r[3],
            "yoga_name": r[4],
            "uploaded_img": r[5],    # file path: /static/saved_images/
            "corrected_img": r[6],   # file path: /static/saved_images/
            "feedback": r[7],
            "date": r[8],
        }
        for r in rows
    ]

    logger.info(f"Dashboard loaded: {user_email} ({len(sessions_data)} sessions)")
    return render_template(
        "dashboard.html",
        user_name=user_name,
        dashboard_data=sessions_data,
        stats=stats,
    )


@dashboard_bp.route("/chatbot")
@login_required
def chatbot():
    """Display chatbot interface with welcome message."""
    welcome = build_welcome_payload()
    session["chatbot_state"] = welcome.get("state", {})
    logger.info(f"Chatbot opened by: {session.get('user_email')}")
    return render_template(
        "chatbot.html",
        welcome_message=welcome["reply"],
        starter_prompts=welcome["suggestions"],
    )




@dashboard_bp.route("/chatbot/message", methods=["POST"])
@login_required
def chatbot_message():
    """Handle chatbot conversation.
    
    POST endpoint that accepts JSON with user message and returns
    chatbot response with suggestions for next interaction.
    """
    try:
        payload = request.get_json(silent=True) or {}
        message = str(payload.get("message", "")).strip()
        current_state = session.get("chatbot_state", {})
        
        chat_payload = generate_chat_payload(message, current_state)
        session["chatbot_state"] = chat_payload.get("state", current_state)
        
        logger.debug(f"Chatbot response for {session.get('user_email')}")
        return jsonify(
            {
                "reply": chat_payload["reply"],
                "suggestions": chat_payload.get("suggestions", []),
            }
        )
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        return jsonify({"error": "Failed to process message"}), 500
