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

# Configure matplotlib early to prevent hangs
os.environ['MPLBACKEND'] = 'Agg'

try:
    # Initialize ml (will configure matplotlib)
    import ml
    from app import create_app
    env = os.getenv("FLASK_ENV", "production")
    app = create_app(env)
except Exception as e:
    print(f"ERROR: Failed to create app: {e}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=False,
        threaded=True
    )