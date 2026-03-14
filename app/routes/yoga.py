"""
Yoga routes: pose detection, history, and testing.

Provides endpoints for:
- Pose detection testing
- Viewing pose history
- Accessing pose catalogue
"""

from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..extensions import db
from ..models import YogaPose, UserPoseHistory
import logging

logger = logging.getLogger(__name__)
yoga_bp = Blueprint('yoga', __name__)


@yoga_bp.route('/poses')
@login_required
def poses():
    """Display all available yoga poses."""
    try:
        poses = YogaPose.query.order_by(YogaPose.difficulty_level).all()
        return render_template('yoga/poses.html', poses=poses)
    except Exception as e:
        logger.error(f"Error loading poses: {e}")
        flash('Failed to load poses.', 'error')
        return redirect(url_for('dashboard.home'))


@yoga_bp.route('/pose/<int:pose_id>')
@login_required
def pose_detail(pose_id):
    """Display detailed information about a specific pose."""
    try:
        pose = YogaPose.query.get_or_404(pose_id)
        
        # Get user's performance history for this pose
        history = UserPoseHistory.query.filter_by(
            user_id=current_user.id,
            pose_id=pose_id
        ).order_by(UserPoseHistory.performed_at.desc()).all()
        
        # Calculate statistics
        avg_score = 0
        attempts = len(history)
        if attempts > 0:
            avg_score = sum(h.accuracy_score for h in history) / attempts
        
        return render_template(
            'yoga/pose_detail.html',
            pose=pose,
            history=history[:10],  # Last 10 attempts
            avg_score=avg_score,
            attempts=attempts
        )
    except Exception as e:
        logger.error(f"Error loading pose detail: {e}")
        flash('Failed to load pose details.', 'error')
        return redirect(url_for('yoga.poses'))


@yoga_bp.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    """Pose detection page (UI for testing poses)."""
    try:
        poses = YogaPose.query.all()
        return render_template('yoga/detect.html', poses=poses)
    except Exception as e:
        logger.error(f"Error loading detect page: {e}")
        flash('Failed to load pose detection.', 'error')
        return redirect(url_for('dashboard.home'))


@yoga_bp.route('/api/record-pose', methods=['POST'])
@login_required
def record_pose():
    """Record a completed pose attempt."""
    try:
        data = request.get_json()
        pose_id = data.get('pose_id')
        accuracy_score = data.get('accuracy_score', 0)
        duration_seconds = data.get('duration', 0)
        feedback = data.get('feedback', '')
        
        if not pose_id:
            return jsonify({'error': 'Pose ID is required'}), 400
        
        # Verify pose exists
        pose = YogaPose.query.get_or_404(pose_id)
        
        # Record history
        history = UserPoseHistory(
            user_id=current_user.id,
            pose_id=pose_id,
            accuracy_score=accuracy_score,
            duration_seconds=duration_seconds,
            feedback=feedback
        )
        
        db.session.add(history)
        db.session.commit()
        
        logger.info(f"Pose recorded: user={current_user.id}, pose={pose_id}, score={accuracy_score}")
        
        return jsonify({
            'success': True,
            'message': 'Pose recorded successfully',
            'history_id': history.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error recording pose: {e}")
        return jsonify({'error': str(e)}), 500


@yoga_bp.route('/history')
@login_required
def history():
    """View personal pose history."""
    try:
        page = request.args.get('page', 1, type=int)
        history = UserPoseHistory.query.filter_by(user_id=current_user.id).order_by(
            UserPoseHistory.performed_at.desc()
        ).paginate(page=page, per_page=20)
        
        return render_template('yoga/history.html', history=history)
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        flash('Failed to load history.', 'error')
        return redirect(url_for('dashboard.home'))
