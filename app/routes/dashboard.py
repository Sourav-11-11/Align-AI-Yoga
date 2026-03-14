"""
Dashboard routes: user dashboard with statistics and recommendations.

Provides:
- Dashboard home with overview
- Statistics and performance metrics
- AI recommendations display
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import UserPoseHistory, Recommendation, YogaPose
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/home')
@login_required
def home():
    """Main dashboard page."""
    try:
        # Get user statistics
        total_attempts = UserPoseHistory.query.filter_by(user_id=current_user.id).count()
        
        # Get today's attempts
        today = datetime.utcnow().date()
        today_attempts = UserPoseHistory.query.filter(
            UserPoseHistory.user_id == current_user.id,
            UserPoseHistory.performed_at >= today
        ).count()
        
        # Get average accuracy score
        history = UserPoseHistory.query.filter_by(user_id=current_user.id).all()
        avg_score = 0
        if history:
            avg_score = sum(h.accuracy_score for h in history) / len(history)
        
        # Get recent pose history
        recent_history = UserPoseHistory.query.filter_by(
            user_id=current_user.id
        ).order_by(UserPoseHistory.performed_at.desc()).limit(10).all()
        
        # Get latest recommendations
        latest_recommendation = Recommendation.query.filter_by(
            user_id=current_user.id
        ).order_by(Recommendation.generated_at.desc()).first()
        
        recommended_poses = []
        if latest_recommendation and latest_recommendation.recommended_pose_ids:
            recommended_poses = YogaPose.query.filter(
                YogaPose.id.in_(latest_recommendation.recommended_pose_ids)
            ).all()
        
        stats = {
            'total_attempts': total_attempts,
            'today_attempts': today_attempts,
            'avg_score': round(avg_score, 1),
            'streak_days': calculate_streak(current_user.id),
        }
        
        return render_template(
            'dashboard/home.html',
            stats=stats,
            recent_history=recent_history,
            recommended_poses=recommended_poses,
            latest_recommendation=latest_recommendation
        )
        
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        flash('Failed to load dashboard.', 'error')
        return redirect(url_for('index'))


@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('dashboard/profile.html', user=current_user)


@dashboard_bp.route('/stats')
@login_required
def stats():
    """Detailed statistics page."""
    try:
        # Get all history
        history = UserPoseHistory.query.filter_by(user_id=current_user.id).all()
        
        # Group by pose
        pose_stats = {}
        for h in history:
            pose_id = h.pose_id
            if pose_id not in pose_stats:
                pose = YogaPose.query.get(pose_id)
                pose_stats[pose_id] = {
                    'pose': pose,
                    'attempts': 0,
                    'avg_score': 0,
                    'total_score': 0
                }
            pose_stats[pose_id]['attempts'] += 1
            pose_stats[pose_id]['total_score'] += h.accuracy_score
        
        # Calculate averages
        for stats_data in pose_stats.values():
            if stats_data['attempts'] > 0:
                stats_data['avg_score'] = round(stats_data['total_score'] / stats_data['attempts'], 1)
        
        return render_template('dashboard/stats.html', pose_stats=pose_stats)
        
    except Exception as e:
        logger.error(f"Error loading stats: {e}")
        flash('Failed to load statistics.', 'error')
        return redirect(url_for('dashboard.home'))


def calculate_streak(user_id: int) -> int:
    """Calculate current practice streak in days."""
    try:
        today = datetime.utcnow().date()
        current_streak = 0
        
        # Check each day going backwards
        for i in range(365):  # Check up to 1 year
            check_date = today - timedelta(days=i)
            
            count = UserPoseHistory.query.filter(
                UserPoseHistory.user_id == user_id,
                UserPoseHistory.performed_at >= check_date,
                UserPoseHistory.performed_at < check_date + timedelta(days=1)
            ).count()
            
            if count > 0:
                current_streak += 1
            else:
                # Stop if no activity found
                if current_streak > 0:
                    break
        
        return current_streak
        
    except Exception as e:
        logger.error(f"Error calculating streak: {e}")
        return 0
