"""
Database initialization and management helper.

Usage:
    python manage.py init       # Initialize database with tables
    python manage.py seed       # Add sample yoga poses
    python manage.py create-admin <email> <password>  # Create admin user
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, YogaPose


def init_db():
    """Initialize database: create all tables."""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")


def seed_poses():
    """Add sample yoga poses to database."""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    with app.app_context():
        if YogaPose.query.first():
            print("Poses already exist in database")
            return
        
        poses = [
            {
                'pose_name': 'Child Pose',
                'sanskrit_name': 'Balasana',
                'description': 'Resting pose that gently stretches the hips and lower back',
                'difficulty_level': 'Beginner',
                'benefits': 'Relieves stress and fatigue, stretches hip flexors',
                'precautions': 'Avoid if pregnant or have knee injuries',
                'duration_seconds': 30
            },
            {
                'pose_name': 'Downward Dog',
                'sanskrit_name': 'Adho Mukha Svanasana',
                'description': 'Inverted V-shaped pose that strengthens arms and stretches hamstrings',
                'difficulty_level': 'Beginner',
                'benefits': 'Strengthens shoulders, builds core strength, improves flexibility',
                'precautions': 'Avoid if you have shoulder injuries',
                'duration_seconds': 30
            },
            {
                'pose_name': 'Mountain Pose',
                'sanskrit_name': 'Tadasana',
                'description': 'Standing pose that improves posture and balance',
                'difficulty_level': 'Beginner',
                'benefits': 'Improves posture, strengthens thighs and ankles',
                'precautions': 'None',
                'duration_seconds': 20
            },
            {
                'pose_name': 'Cobra Pose',
                'sanskrit_name': 'Bhujangasana',
                'description': 'Backbend that strengthens the spine and abs',
                'difficulty_level': 'Beginner',
                'benefits': 'Strengthens arms and chest, opens the heart',
                'precautions': 'Avoid if you have back pain or wrist injuries',
                'duration_seconds': 30
            },
            {
                'pose_name': 'Tree Pose',
                'sanskrit_name': 'Vrikshasana',
                'description': 'Standing balance pose that improves focus and stability',
                'difficulty_level': 'Intermediate',
                'benefits': 'Improves balance and focus, strengthens legs',
                'precautions': 'Avoid if you have ankle problems',
                'duration_seconds': 30
            },
        ]
        
        for pose_data in poses:
            pose = YogaPose(**pose_data)
            db.session.add(pose)
        
        db.session.commit()
        print(f"✓ Added {len(poses)} yoga poses to database")


def create_admin(email, password, name="Admin"):
    """Create an admin user."""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"✗ User with email {email} already exists")
            return
        
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"✓ Admin user created: {email}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        init_db()
    elif command == 'seed':
        seed_poses()
    elif command == 'create-admin':
        if len(sys.argv) < 4:
            print("Usage: python manage.py create-admin <email> <password> [name]")
            sys.exit(1)
        email = sys.argv[2]
        password = sys.argv[3]
        name = sys.argv[4] if len(sys.argv) > 4 else "Admin"
        create_admin(email, password, name)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

