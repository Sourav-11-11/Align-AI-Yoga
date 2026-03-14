"""
Local development entry point for Align AI Yoga.

Run locally with:
    flask run

Or with this script:
    python run.py

Environment variables are loaded from .env file automatically.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

if __name__ == '__main__':
    # Create app with development config
    app = create_app('development')
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✓ Database tables initialized")
    
    print("🧘 Starting Align AI Yoga - Development Server")
    print("📍 Running on http://localhost:5000")
    print("Press CTRL+C to quit")
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
