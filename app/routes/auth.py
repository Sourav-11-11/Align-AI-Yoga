"""
Authentication routes: register, login, logout.

Provides user account management with secure password hashing
and Flask-Login session management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            # Validation
            if not name or not email or not password:
                flash('All fields are required.', 'error')
                return render_template('register.html'), 400
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'error')
                return render_template('register.html'), 400
            
            if password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('register.html'), 400
            
            # Check if user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered.', 'error')
                return render_template('register.html'), 400
            
            # Create new user
            user = User(name=name, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"New user registered: {email}")
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {e}")
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html'), 500
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            
            if not email or not password:
                flash('Email and password are required.', 'error')
                return render_template('login.html'), 400
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user, remember=request.form.get('remember', False))
                logger.info(f"User logged in: {email}")
                
                # Redirect to next page or dashboard
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('dashboard.home'))
            
            flash('Invalid email or password.', 'error')
            return render_template('login.html'), 401
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            flash(f'Login failed: {str(e)}', 'error')
            return render_template('login.html'), 500
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout endpoint."""
    logger.info(f"User logged out: {current_user.email}")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
