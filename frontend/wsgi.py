"""
WSGI entry point for Gunicorn.

This allows Gunicorn to run the Flask app in production.
Usage: gunicorn wsgi:app
"""

from app import create_app

app = create_app('production')

if __name__ == "__main__":
    app.run()
