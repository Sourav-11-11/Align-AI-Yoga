"""
Entry point for CSP Align AI – Yoga Pose Recognition & Recommendation System.

Usage:
    python run.py
"""

import os
import sys

# Add frontend directory to Python path so ml module can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

env = os.getenv("FLASK_ENV", "development")
app = create_app(env)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)