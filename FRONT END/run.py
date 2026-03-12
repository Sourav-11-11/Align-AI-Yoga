"""
Entry point for CSP Align AI – Yoga Pose Recognition & Recommendation System.

Usage:
    python run.py
"""

import os
from app import create_app

env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
