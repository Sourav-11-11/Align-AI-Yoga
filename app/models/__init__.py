"""
Database models for Align AI Yoga application.

SQLAlchemy ORM models for:
- User accounts with authentication
- Yoga poses catalogue
- User pose history tracking
- AI recommendations
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(UserMixin, db.Model):
    """User account model with authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    pose_history = db.relationship('UserPoseHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.email}>'


class YogaPose(db.Model):
    """Yoga pose catalogue."""
    __tablename__ = 'yoga_poses'

    id = db.Column(db.Integer, primary_key=True)
    pose_name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    sanskrit_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(50))  # e.g., Beginner, Intermediate, Advanced
    benefits = db.Column(db.Text)
    precautions = db.Column(db.Text)
    duration_seconds = db.Column(db.Integer, default=30)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    history_records = db.relationship('UserPoseHistory', backref='pose', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<YogaPose {self.pose_name}>'


class UserPoseHistory(db.Model):
    """Track user's yoga pose attempts and performance."""
    __tablename__ = 'user_pose_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    pose_id = db.Column(db.Integer, db.ForeignKey('yoga_poses.id'), nullable=False, index=True)
    accuracy_score = db.Column(db.Float, default=0.0)  # 0-100 percentage
    duration_seconds = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    performed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self) -> str:
        return f'<UserPoseHistory user_id={self.user_id} pose_id={self.pose_id}>'


class Recommendation(db.Model):
    """AI-generated yoga recommendations for users."""
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Store multiple recommended pose IDs as JSON
    recommended_pose_ids = db.Column(db.JSON, default=list)
    recommendation_reason = db.Column(db.Text)
    
    # Metadata
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime)  # When recommendation expires
    viewed = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Recommendation user_id={self.user_id}>'
