"""
WSGI entry point for production deployment on Render/Gunicorn.

Use this for production:
    gunicorn wsgi:app

For local development, use run.py instead:
    flask run
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

# Create the Flask app instance
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    app.run()
