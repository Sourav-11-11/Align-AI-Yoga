"""
Flask application factory.

Centralises all app setup: config, blueprints, and teardown hooks.
Using the Application Factory pattern makes the app easier to test
and allows multiple configurations (dev, prod, test).
"""

import os
import sys
from flask import Flask, g
from .config import config


def create_app(env: str = "default") -> Flask:
    """Create and configure the Flask app."""
    try:
        app = Flask(
            __name__,
            template_folder=os.path.join(os.path.dirname(__file__), "../templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "../static"),
        )

        # Load config class
        app.config.from_object(config[env])

        # Ensure critical directories exist
        os.makedirs(app.config["SAVED_IMAGES_DIR"], exist_ok=True)
        os.makedirs(os.path.join(app.static_folder, "img"), exist_ok=True)

        # Register blueprints
        from .routes.auth import auth_bp
        from .routes.yoga import yoga_bp
        from .routes.dashboard import dashboard_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(yoga_bp)
        app.register_blueprint(dashboard_bp)

        # Teardown: close DB connection after each request
        @app.teardown_appcontext
        def close_db(exception=None):
            db = g.pop("db", None)
            if db is not None and db.is_connected():
                db.close()

        return app
    except Exception as e:
        print(f"ERROR in create_app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise
