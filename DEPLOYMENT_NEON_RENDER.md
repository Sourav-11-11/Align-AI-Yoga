# Align AI Yoga - Deployment Guide (Neon + Render)

## Overview

This guide explains how to deploy Align AI Yoga on Render with a free PostgreSQL database from Neon.

**Cost: $0/month** (Free tier)
- Render: Web service (512 MB RAM, 0.5 CPU)
- Neon: PostgreSQL database (free tier with generous limits)

---

## Prerequisites

1. GitHub account (for source code)
2. Render account ([render.com](https://render.com)) - **Sign up with GitHub**
3. Neon account ([neon.tech](https://neon.tech)) - **Sign up with GitHub**

---

## Step 1: Set Up PostgreSQL Database on Neon

### 1.1 Create Neon Project

1. Go to [neon.tech](https://neon.tech)
2. Click "Sign up" → "Continue with GitHub"
3. Authorize Neon
4. Click "+ New Project"
5. Choose:
   - **Database name**: `align-yoga-db`
   - **Region**: Choose closest to your location
   - **PostgreSQL version**: Latest (15.x or 16.x)
6. Click "Create project"

### 1.2 Get Connection String

1. Go to "Connection strings" tab
2. Copy the **psql Connection URL** (psycopg2 format)
   - Format: `postgresql://user:password@host/database`
3. **Save this safely** - you'll use it later

Example:
```
postgresql://neon_user:AbC123xyz@ep-small-frost-123456.us-east-4.neon.tech/align-yoga-db
```

---

## Step 2: Prepare Your Code on GitHub

### 2.1 Ensure Your Repo Structure

```
align-ai-yoga/
├── app/                    # Flask app package
│   ├── __init__.py         # App factory
│   ├── config.py           # Configuration
│   ├── extensions.py       # DB, Login extensions
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # Blueprint routes
│   ├── services/           # Business logic
│   ├── templates/          # HTML templates (your existing ones!)
│   └── static/             # CSS, JS (your existing ones!)
├── requirements.txt        # Dependencies
├── wsgi.py                # Gunicorn entry point (production)
├── run.py                 # Local development entry point
├── manage.py              # Database setup helper
├── Procfile               # Render deployment config
├── .env.example           # Template for environment variables
└── README.md
```

### 2.2 Update requirements.txt

Your new requirements.txt should have:
```
Flask>=3.0
Flask-SQLAlchemy>=3.1
SQLAlchemy>=2.0
psycopg2-binary>=2.9
Flask-Login>=0.6
Flask-Migrate>=4.0
gunicorn>=21.2
python-dotenv>=1.0
```

### 2.3 Create .env.example

```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/align_yoga_dev
```

**Important:** Add `.env` (actual values) to `.gitignore` - Never commit real secrets!

### 2.4 Commit and Push

```bash
git add apps/ requirements.txt wsgi.py run.py manage.py .env.example Procfile
git commit -m "refactor: migrate to PostgreSQL and Render deployment"
git push origin main
```

---

## Step 3: Deploy on Render

### 3.1 Connect Render to GitHub

1. Go to [render.com/dashboard](https://render.com/dashboard)
2. Click "+ New" → "Web Service"
3. Click "Connect" next to your GitHub repo
4. Search for `align-ai-yoga` (or your repo name)
5. Click "Connect"

### 3.2 Configure Render Service

1. **Name**: `align-ai-yoga`
2. **Environment**: `Python 3`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn wsgi:app`
5. **Instance Type**: Free (512 MB, 0.5 CPU)

### 3.3 Add Environment Variables

1. Scroll down to "Environment" section
2. Add these variables:

   | Key | Value |
   |-----|-------|
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | Generate a random string (or use: `python -c "import secrets; print(secrets.token_hex(32))"`) |
   | `DATABASE_URL` | Paste your Neon connection string from Step 1.2 |

3. Click "Save"

### 3.4 Deploy

1. Click "Create Web Service"
2. Render will:
   - Clone your repo
   - Install dependencies
   - Start the app
3. Wait ~3-5 minutes for deployment
4. Check logs for any errors
5. Once successful, you'll get a URL: `https://align-ai-yoga.onrender.com`

---

## Step 4: Initialize Database

Once deployed, you need to initialize the database with tables and sample data.

### Option A: Using render.sh Script (Recommended)

1. Create `render.sh` in your project root:
   ```bash
   #!/bin/bash
   set -eu

   pip install -r requirements.txt
   python manage.py init
   python manage.py seed
   
   echo "✓ Database initialized!"
   ```

2. Make it executable:
   ```bash
   chmod +x render.sh
   ```

3. Update **Render Settings**:
   - Go to your service settings
   - Change **Build Command** to: `bash render.sh`

4. Redeploy

### Option B: Using SSH (Manual)

1. Click your Render service
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py init
   python manage.py seed
   ```

---

## Step 5: Test Your Deployment

1. Open your Render URL: `https://align-ai-yoga.onrender.com`
2. Test the following:
   - ✅ **Home page** loads
   - ✅ **Register** - Create an account
   - ✅ **Login** - Log in with your account
   - ✅ **Dashboard** - View your profile
   - ✅ **Pose list** - See available poses

---

## Local Development

### Setup Local Environment

1. **Create .env file** (copy from .env.example):
   ```bash
   cp .env.example .env
   ```

2. **Edit .env** with local database:
   ```
   FLASK_ENV=development
   SECRET_KEY=dev-secret
   DATABASE_URL=postgresql://postgres:password@localhost:5432/align_yoga_dev
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize local database**:
   ```bash
   python manage.py init
   python manage.py seed
   ```

5. **Run locally**:
   ```bash
   python run.py
   ```

   Or:
   ```bash
   flask run
   ```

6. Open `http://localhost:5000`

---

## Troubleshooting

### Database Connection Failed

**Error**: `psycopg2.OperationalError: connection failed`

**Solution**:
1. Check DATABASE_URL in Render environment variables
2. Verify Neon project still exists
3. Test connection locally: `psql <your-connection-string>`

### "No module named 'psycopg2'"

**Solution**: Render must install `psycopg2-binary` (not `psycopg2`)
- Ensure `requirements.txt` has `psycopg2-binary>=2.9`

### App Won't Start

**Solution**: Check Render logs:
1. Go to your service
2. Click "Logs" tab
3. Look for error messages
4. Common issues:
   - `SECRET_KEY` not set
   - `DATABASE_URL` invalid format
   - Python version mismatch (should be 3.9+)

### Tables Already Exist

**Error**: When running `python manage.py init` again

**Solution**: Tables persist (this is good!). Your data is safe.

---

## Connecting to Production Database from Local PC

If you need to query your Neon database from your computer:

```bash
# Install psql (PostgreSQL client)
# Then run:
psql "postgresql://user:password@neon-host/align-yoga-db"
```

Or use a GUI like DBeaver:
1. Download [DBeaver Community](https://dbeaver.io)
2. New Database Connection
3. PostgreSQL
4. Enter Neon connection details
5. Test connection

---

## Scaling & Next Steps

### Free Tier Limits (Neon)
- 3 projects
- 3 GB storage per project
- Some compute time limits
- **Sufficient for portfolio projects**

### Free Tier Limits (Render)
- App sleeps after 15 mins inactivity
- ~4 hours sleep per month
- **Okay for portfolio/demo**

### To Make Paid (Optional)
- **Neon Pro**: $14/month for unlimited projects
- **Render**: $12/month for always-on service

---

## File Reference

| File | Purpose |
|------|---------|
| `app/__init__.py` | Flask app factory |
| `app/config.py` | Configuration for dev/prod |
| `app/extensions.py` | SQLAlchemy & Flask-Login init |
| `app/models/__init__.py` | SQLAlchemy ORM models |
| `app/routes/auth.py` | Login/register routes |
| `app/routes/yoga.py` | Yoga pose routes |
| `app/routes/dashboard.py` | User dashboard |
| `wsgi.py` | Production entry point (gunicorn) |
| `run.py` | Local development entry point |
| `manage.py` | Database setup helper |
| `Procfile` | Render deployment config |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

---

## Support

For issues:
1. Check Render logs (Settings → Logs tab)
2. Check local logs (`python run.py`)
3. Test database connection locally
4. Review SQLAlchemy documentation
5. Check [Neon docs](https://neon.tech/docs)

---

**You're all set! 🚀**

Your Align AI Yoga app is now deployed on Render with a free PostgreSQL database. Share your live URL with recruiters!
