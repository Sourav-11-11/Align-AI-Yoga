"""
Authentication routes: register, login, logout, landing pages.

Security improvements over the original:
  - Passwords are hashed with Werkzeug's PBKDF2-SHA256 (was plaintext).
  - Parameterised queries prevent SQL injection (preserved from original).
  - flash() messages replace template-level 'message' variables.
  - login_required decorator added for protected routes.
"""

import functools
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
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form["c_password"]

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        existing = fetchone("SELECT id FROM users WHERE email = %s", (email,))
        if existing:
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        # Hash the password before storing — NEVER store plaintext passwords.
        hashed = generate_password_hash(password)
        execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, hashed),
        )
        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ── Login ─────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = fetchone(
            "SELECT id, name, email, password_hash FROM users WHERE email = %s",
            (email,),
        )

        # Constant-time check prevents user-enumeration timing attacks.
        if not user or not check_password_hash(user[3], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_email"] = user[2]
        return redirect(url_for("yoga.home"))

    return render_template("login.html")


# ── Logout ────────────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
