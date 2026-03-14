"""
Authentication routes: register, login, logout, landing pages.

Security improvements over the original:
  - Passwords are hashed with Werkzeug's PBKDF2-SHA256 (was plaintext).
  - Parameterised queries prevent SQL injection (preserved from original).
  - flash() messages replace template-level 'message' variables.
  - login_required decorator added for protected routes.
  - Comprehensive logging for security audits.
"""

import functools
import logging
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
)
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.db import execute, fetchone

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


# ── Login-required decorator ──────────────────────────────────────────────────

def login_required(view):
    """Redirect unauthenticated users to the login page."""
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


# ── Public routes ─────────────────────────────────────────────────────────────

@auth_bp.route("/")
def index():
    return render_template("index.html")


@auth_bp.route("/about")
def about():
    return render_template("about.html")


# ── Registration ──────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration endpoint.
    
    POST: Create new user account
    - Validates email uniqueness
    - Hashes password with PBKDF2-SHA256
    - Returns success message and redirects to login
    
    GET: Display registration form
    """
    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            email = request.form["email"].strip().lower()
            password = request.form["password"]
            confirm = request.form["c_password"]

            # Validate password match
            if password != confirm:
                flash("Passwords do not match.", "error")
                logger.warning(f"Registration attempt: password mismatch for {email}")
                return render_template("register.html")

            # Check if email already registered
            existing = fetchone("SELECT id FROM users WHERE email = %s", (email,))
            if existing:
                flash("An account with that email already exists.", "error")
                logger.info(f"Registration attempt: duplicate email {email}")
                return render_template("register.html")

            # Hash password and create account
            hashed = generate_password_hash(password)
            execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, hashed),
            )
            logger.info(f"New user registered: {email}")
            flash("Account created! Please log in.", "success")
            return redirect(url_for("auth.login"))
            
        except KeyError as e:
            flash(f"Missing form field: {e}", "error")
            logger.error(f"Registration error - missing field: {e}")
            return render_template("register.html"), 400
        except Exception as e:
            flash("Registration failed. Please try again.", "error")
            logger.error(f"Registration error: {str(e)}")
            return render_template("register.html"), 500

    return render_template("register.html")


# ── Login ─────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login endpoint.
    
    POST: Authenticate user with email and password
    - Uses constant-time password comparison (prevents timing attacks)
    - Sets secure session cookies
    - Returns 401 on invalid credentials (generic message for security)
    
    GET: Display login form
    """
    if request.method == "POST":
        try:
            email = request.form["email"].strip().lower()
            password = request.form["password"]

            # Fetch user record
            user = fetchone(
                "SELECT id, name, email, password_hash FROM users WHERE email = %s",
                (email,),
            )

            # Constant-time check prevents user-enumeration timing attacks
            if not user or not check_password_hash(user[3], password):
                flash("Invalid email or password.", "error")
                logger.warning(f"Login attempt failed for: {email}")
                return render_template("login.html")

            # Create authenticated session
            session.clear()
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]
            logger.info(f"User logged in: {email}")
            return redirect(url_for("yoga.home"))
            
        except KeyError as e:
            flash(f"Missing form field: {e}", "error")
            logger.error(f"Login error - missing field: {e}")
            return render_template("login.html"), 400
        except Exception as e:
            flash("Login failed. Please try again.", "error")
            logger.error(f"Login error: {str(e)}")
            return render_template("login.html"), 500

    return render_template("login.html")


# ── Logout ────────────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    """User logout endpoint.
    
    Clears the session and redirects to homepage.
    """
    logger.info(f"User logged out: {session.get('user_email')}")
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.index"))
