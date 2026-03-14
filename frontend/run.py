"""
Entry point for CSP Align AI – Yoga Pose Recognition & Recommendation System.

Usage:
    python run.py
"""

import os
import sys
import traceback

# Add frontend directory to Python path so ml module can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    env = os.getenv("FLASK_ENV", "development")
    app = create_app(env)
except Exception as e:
    print(f"ERROR: Failed to create app: {e}")
    traceback.print_exc()
    raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
else:
    # For Gunicorn/production server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)