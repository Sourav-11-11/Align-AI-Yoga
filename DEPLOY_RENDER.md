# Deploying Align AI Yoga to Render

This guide walks through deploying the Align AI Yoga application to Render using SQLite as the database.

## Prerequisites

1. A [Render account](https://render.com) (free tier available)
2. This repository pushed to GitHub
3. A GitHub account with push access to the repo

## Quick Start: Deploy in 5 Minutes

### Step 1: Connect Repository to Render

1. Log in to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a repository"**
4. Find and select this repository: `ALIGN AI YOGA`
5. Click **"Connect"**

### Step 2: Configure the Web Service

Fill in the following fields:

| Field | Value |
|-------|-------|
| **Name** | `align-ai-yoga` (or your preferred name) |
| **Environment** | `Python 3` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `cd frontend && gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 60 wsgi:app` |

### Step 3: Environment Variables

Add these environment variables in the **"Environment"** section:

```
FLASK_ENV=production
SECRET_KEY=your-long-random-secret-key-here
DB_TYPE=sqlite
```

> **Tip:** Generate a secure `SECRET_KEY` using Python:
> ```python
> import secrets
> print(secrets.token_urlsafe(32))
> ```

### Step 4: Deploy

Click **"Create Web Service"** and wait for the deployment to complete (~3-5 minutes).

## How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│         Render (Hosting)                │
│ ┌───────────────────────────────────┐   │
│ │  Flask App (/frontend)            │   │
│ │  • Routes (auth, yoga, dashboard) │   │
│ │  • ML Services (MediaPipe)         │   │
│ │  • Templates (11 HTML files)       │   │
│ ├───────────────────────────────────┤   │
│ │  SQLite Database                  │   │
│ │  • On-disk: align_yoga.db         │   │
│ │  • Persisted between restarts      │   │
│ └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Database: SQLite

- **No external database needed** (eliminates setup friction)
- **Persistent storage** (database file is preserved between deployments)
- **Works on free tier** (unlike PostgreSQL which requires $7/month tier)
- Database file location: `/frontend/align_yoga.db`

### Environment Setup

Your app automatically initializes with:
- **SQLite database** (`DB_TYPE=sqlite` by default in production)
- **Admin tables** created on first startup
- **User authentication system** (login, register)
- **Yoga pose tracking** (history, recommendations)

## After Deployment

### Test Your App

1. Visit your deployment URL (e.g., `https://align-ai-yoga.onrender.com`)
2. Create an account at `/auth/register`
3. Log in at `/auth/login`
4. Access the dashboard at `/dashboard`

### Common Issues

| Issue | Solution |
|-------|----------|
| **502 Bad Gateway** | App is still building; wait 3-5 minutes |
| **500 Internal Server Error** | Check Render logs (View Logs button) for detailed errors |
| **Database connection error** | Verify `FLASK_ENV=production` and `DB_TYPE=sqlite` in environment |
| **Static files not loading** | Handled automatically by Flask; no separate CDN needed |

### Check Logs

In Render dashboard:
1. Click your service
2. Click **"Logs"** tab
3. Look for `ERROR`, `WARNING`,  or connection messages

### Database Persistence

SQLite database is persistent:
- Survives app restarts and redeployments
- Stored in the ephemeral filesystem (per Render docs)
- **Backup important data** to a secondary source if needed
- For production use, consider migrating to Render PostgreSQL ($7/month)

## Local Development

### Run Locally

```bash
cd frontend
python run.py
# Visit http://localhost:5000
```

### Switch to Local SQLite

```bash
# .env (create if doesn't exist)
FLASK_ENV=development
DB_TYPE=sqlite
```

### Switch to Local MySQL (if available)

```bash
# .env
FLASK_ENV=development
DB_TYPE=mysql
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_PORT=3306
DB_NAME=yoga
```

## Production Best Practices

### 1. Secure Your Secrets

```bash
# Generate a strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to Render environment variables
SECRET_KEY=<generated_key>
```

### 2. Monitoring

- Enable **"Auto-Deploy on Push"** for continuous deployment
- Set up alerts for failed builds in Render dashboard

### 3. Scaling Up Later

When you're ready for production scale:
- Upgrade to **Render PostgreSQL** ($7/month) for reliable multi-instance deployment
- Implement **Redis caching** for ML inference results
- Use **CDN** for static files

### 4. Environment Configuration

Your app respects these env vars:

| Variable | Default | Options |
|----------|---------|---------|
| `FLASK_ENV` | development | development, production |
| `DB_TYPE` | sqlite | sqlite, mysql |
| `SECRET_KEY` | random | Any secure string |
| `PORT` | 5000 | Any valid port |

## Updating Your App

### Deploy Updates

```bash
# Make changes locally
git add .
git commit -m "your changes"
git push origin main

# Render auto-deploys if enabled
# Otherwise, manually trigger via Render dashboard
```

### Database Migrations

⚠️ **Note:** SQLite schema updates happen automatically on app startup via `_create_sqlite_tables()` in `frontend/app/utils/db.py`

## Troubleshooting

### App builds but doesn't start

Check these:
1. `FLASK_ENV=production` is set
2. `SECRET_KEY` is set (non-empty string)
3. Build command completed successfully
4. Start command is: `cd frontend && gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 60 wsgi:app`

### Database not persisting

SQLite persists by default. If data is lost:
1. Check Render restart/redeployment didn't happen
2. Look for database errors in logs
3. Verify `DB_TYPE=sqlite` in environment

### ML inference is slow

MediaPipe is lazy-loaded to save startup time:
- First inference request (~10s) is slower
- Subsequent requests are normal speed
- For production, increase instance size/concurrency

## Support

- **Render Docs:** https://render.com/docs
- **Flask Docs:** https://flask.palletsprojects.com
- **SQLite Docs:** https://www.sqlite.org/docs.html

---

**Happy deploying! 🧘‍♀️🚀**
