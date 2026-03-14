"""
Flask application factory.

Creates and configures the Flask app with all extensions,
blueprints, and error handlers.
"""

import os
import sys
import logging
from flask import Flask, jsonify
from flask_migrate import Migrate

from .config import get_config
from .extensions import db, login_manager
from .models import User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

migrate = Migrate()


def create_app(config_name: str = None) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Configuration environment ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    try:
        app = Flask(__name__)
        
        # Load configuration
        if config_name is None:
            config_name = os.getenv('FLASK_ENV', 'development')
        
        config = get_config(config_name)
        app.config.from_object(config)
        
        logger.info(f"Creating app with config: {config_name}")
        
        # Initialize extensions
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app, db)
        
        # Load user for Flask-Login
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Create tables if needed
        with app.app_context():
            db.create_all()
        
        # Create upload folder
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Register blueprints
        from .routes.auth import auth_bp
        from .routes.yoga import yoga_bp
        from .routes.dashboard import dashboard_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(yoga_bp, url_prefix='/yoga')
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        
        # Home route
        @app.route('/')
        def index():
            from flask import render_template
            return render_template('index.html')
        
        # Error handlers
        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({'error': 'Bad request', 'message': str(error)}), 400
        
        @app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Not found', 'message': str(error)}), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            logger.error(f"500 Error: {error}", exc_info=True)
            return jsonify({'error': 'Internal server error', 'message': str(error)}), 500
        
        @app.errorhandler(Exception)
        def handle_exception(error):
            logger.error(f"Unhandled exception: {error}", exc_info=True)
            if hasattr(error, 'code'):
                return error
            return jsonify({'error': 'Server error', 'message': str(error)}), 500
        
        logger.info("App created successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to create app: {e}", exc_info=True)
        print(f"ERROR in create_app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise
