"""
Flask application factory.

Centralises all app setup: config, blueprints, and teardown hooks.
Using the Application Factory pattern makes the app easier to test
and allows multiple configurations (dev, prod, test).
"""

import os
import sys
import logging
from flask import Flask, g, jsonify
from .config import config

# Configure logging to see errors in production
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

        # Error handler for 500 Internal Server Error
        @app.errorhandler(500)
        def handle_500(error):
            logger.error(f"500 Error: {error}", exc_info=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return jsonify({
                "error": "Internal Server Error",
                "message": str(error)
            }), 500

        # Error handler for database connection errors
        @app.errorhandler(Exception)
        def handle_exception(error):
            # Pass through HTTP errors
            if hasattr(error, 'code'):
                return error
            logger.error(f"Unhandled Exception: {error}", exc_info=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return jsonify({
                "error": "Server Error",
                "message": str(error)
            }), 500

        return app
    except Exception as e:
        print(f"ERROR in create_app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise
