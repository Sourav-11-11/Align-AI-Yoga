# Align AI Yoga - Backend Structure

## Project Overview

**Align AI Yoga** is a Flask web application for AI-powered yoga pose detection and tracking. This refactored version uses:

- **Framework**: Flask 3.1
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Authentication**: Flask-Login
- **Deployment**: Render + Neon PostgreSQL
- **Server**: Gunicorn (production) / Flask dev server (local)

---

## Quick Start

### Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env
# Edit .env with your DATABASE_URL

# 3. Initialize database
python manage.py init
python manage.py seed

# 4. Run locally
python run.py
```

Visit `http://localhost:5000`

### Production Deployment

See [DEPLOYMENT_NEON_RENDER.md](DEPLOYMENT_NEON_RENDER.md) for complete deployment instructions.

Brief:
```bash
# On Render, it automatically:
gunicorn wsgi:app
```

---

## Project Structure

```
app/
├── __init__.py              # Flask app factory (create_app)
├── config.py                # Configuration (Dev, Prod, Test)
├── extensions.py            # SQLAlchemy & Flask-Login initialization
│
├── models/
│   └── __init__.py          # SQLAlchemy ORM models
│       - User
│       - YogaPose
│       - UserPoseHistory
│       - Recommendation
│
├── routes/
│   ├── auth.py              # Login, register, logout
│   ├── yoga.py              # Pose detection, history
│   └── dashboard.py         # User dashboard
│
├── services/                # Business logic (future)
│   └── __init__.py
│
├── templates/               # HTML templates
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Home page
│   ├── login.html           # Login form
│   ├── register.html        # Registration form
│   ├── dashboard/           # Dashboard pages
│   └── yoga/                # Yoga pages
│
└── static/                  # Static files (CSS, JS, images)
    ├── css/
    └── js/

app.py                       # App factory (if needed)
wsgi.py                      # Production entry point (gunicorn)
run.py                       # Local development entry point
manage.py                    # Database management helper
requirements.txt            # Python dependencies
Procfile                    # Render deployment config
.env.example                # Template for environment variables
```

---

## Key Features

### Database Models

#### User
- Email (unique)
- Password (hashed with Werkzeug)
- Name
- Timestamps (created_at, updated_at)
- Relationships: pose_history, recommendations

#### YogaPose
- Pose name (unique)
- Sanskrit name
- Difficulty level (Beginner, Intermediate, Advanced)
- Description, benefits, precautions
- Duration in seconds
- Relationships: history_records

#### UserPoseHistory
- user_id, pose_id (foreign keys)
- accuracy_score (0-100)
- duration_seconds
- feedback text
- performed_at timestamp
- image_path (for pose photos)

#### Recommendation
- user_id (foreign key)
- recommended_pose_ids (JSON array)
- recommendation_reason
- generated_at, expires_at timestamps
- viewed flag

### Routes

#### Authentication (`/auth`)
- `POST /auth/register` - Create account
- `POST /auth/login` - Log in
- `GET /auth/logout` - Log out (requires login)

#### Yoga (`/yoga`)
- `GET /yoga/poses` - List all poses (requires login)
- `GET /yoga/pose/<id>` - Pose details with user history (requires login)
- `GET /yoga/detect` - Pose detection page (requires login)
- `POST /yoga/api/record-pose` - Save pose attempt (requires login)
- `GET /yoga/history` - User's pose history (requires login)

#### Dashboard (`/dashboard`)
- `GET /dashboard/home` - Main dashboard (requires login)
- `GET /dashboard/profile` - User profile (requires login)
- `GET /dashboard/stats` - Detailed statistics (requires login)

#### Public
- `GET /` - Home page (no login required)

---

## Configuration

### Environment Variables

Set these in your `.env` file or Render dashboard:

```
FLASK_ENV=development          # or 'production'
SECRET_KEY=your-secret-key     # Generate: python -c "import secrets; print(secrets.token_hex(32))"
DATABASE_URL=postgresql://...  # From Neon or local PostgreSQL
```

### Config Classes

- **DevelopmentConfig**: Debug=True, local database
- **ProductionConfig**: Debug=False, uses DATABASE_URL env var
- **TestingConfig**: Uses in-memory SQLite

---

## Database Setup

### Initialize Tables

```bash
python manage.py init
```

Creates:
- users
- yoga_poses
- user_pose_history
- recommendations

### Add Sample Poses

```bash
python manage.py seed
```

Adds 5 beginner yoga poses:
- Child Pose
- Downward Dog
- Mountain Pose
- Cobra Pose
- Tree Pose

### Create Admin User

```bash
python manage.py create-admin admin@example.com password123 "Admin User"
```

---

## Authentication Flow

1. User registers with email/password
2. Password hashed with Werkzeug's `generate_password_hash()`
3. User logs in with email/password
4. `check_password_hash()` validates credentials
5. Flask-Login creates session with user_id
6. `@login_required` decorator protects routes
7. User logout clears session

---

## Running Tests

```bash
# Coming soon: Pytest suite
pytest tests/
```

---

## Deployment Checklist

- [ ] DATABASE_URL set in Render dashboard
- [ ] SECRET_KEY set in Render dashboard
- [ ] FLASK_ENV set to production
- [ ] requirements.txt includes all dependencies
- [ ] Database initialized (run manage.py init on Render)
- [ ] Sample poses seeded
- [ ] Test login/register works
- [ ] Test dashboard loads

---

## Common Commands

```bash
# Local development
python run.py

# Using Flask CLI
flask run

# Install dependencies
pip install -r requirements.txt

# Initialize database
python manage.py init

# Seed sample data
python manage.py seed

# Production (Render)
gunicorn wsgi:app

# Create admin user
python manage.py create-admin <email> <password> [name]
```

---

## Troubleshooting

### Database Connection Error
```
psycopg2.OperationalError: connection failed
```
→ Check DATABASE_URL in .env / Render

### "No module named 'app'"
```
ModuleNotFoundError: No module named 'app'
```
→ Run from project root directory

### "No tables found"
```
ProgrammingError: table "users" does not exist
```
→ Run: `python manage.py init`

### Port already in use
```
OSError: [Errno 48] Address already in use
```
→ Change port in run.py or kill the process

---

## Future Enhancements

- [ ] ML model integration (MediaPipe) for pose detection
- [ ] Image upload for pose verification
- [ ] Pose recommendations based on user history
- [ ] Social features (follow, leaderboard)
- [ ] Video tutorials for each pose
- [ ] Mobile app (React Native)
- [ ] WebSocket for real-time feedback

---

## License

MIT License - Feel free to use for portfolio projects

---

## Support

For deployment help, see: [DEPLOYMENT_NEON_RENDER.md](DEPLOYMENT_NEON_RENDER.md)

Built with ❤️ for yoga practitioners and recruiters
