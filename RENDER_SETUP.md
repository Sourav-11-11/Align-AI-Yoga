# IMPORTANT: Setup Instructions for Render Deployment

## Problem: Login/Register Not Working (Internal Server Error)

The "Internal Server Error" on login/register is due to **missing MySQL database configuration on Render**.

The app has been updated with better error handling and logging, so you'll now see what the real error is on Render.

---

## Solution: Set Up MySQL Database

### Step 1: Create MySQL Database on Render or External Provider

**Option A: Use Railway MySQL** (Recommended for Render)
1. Go to [railway.app](https://railway.app)
2. Create a new project with MySQL
3. Copy the connection details:
   - Host
   - Port
   - Username
   - Password
   - Database name

**Option B: Use External MySQL Service**
- Services like Planetscale, AWS RDS, or DigitalOcean MySQL
- Get the connection details in the same way

### Step 2: Initialize the Database Schema

Run the SQL commands from `frontend/database/schema.sql`:

```bash
# Using mysql command line:
mysql -h <HOST> -u <USER> -p<PASSWORD> < frontend/database/schema.sql

# Or using a MySQL GUI (MySQL Workbench, DBeaver, etc.):
# 1. Connect to your MySQL instance
# 2. Create database: CREATE DATABASE IF NOT EXISTS yoga;
# 3. Copy/paste contents of schema.sql and execute
```

This creates:
- `users` table (for login/register)
- `yoga_poses` table
- `user_pose_history` table
- `user_recommendations` table

### Step 3: Set Environment Variables on Render

1. Go to your Render service Settings
2. Click "Environment" tab
3. Add these environment variables:

```
DB_HOST=<your_mysql_host>
DB_PORT=3306
DB_USER=<your_mysql_username>
DB_PASSWORD=<your_mysql_password>
DB_NAME=yoga
```

4. Click "Save"

### Step 4: Redeploy on Render

1. Go to your Render service
2. Click "Manual Deploy" or wait for auto-deploy
3. Check the deployment logs - should now see:
   - "Database connection established successfully" ✅
   - App listening on PORT ✅
   - NO "ModuleNotFoundError" ✅

### Step 5: Test Login/Register

1. Open your Render app URL
2. Click "Register" 
3. Create a new account
4. You should see "Account created! Please log in."
5. Click "Login"
6. Enter your credentials
7. Should redirect to home page ✅

---

## Troubleshooting

### Still seeing "Internal Server Error"?

Check Render deployment logs for the exact error:

1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. Look for lines starting with "ERROR in create_app:" or database connection errors

**Common errors:**
- `Connection refused` → Database host/port is wrong
- `Access denied for user` → Wrong username/password
- `Unknown database 'yoga'` → Database not created yet
- `Table 'yoga.users' doesn't exist` → Schema.sql not executed

### Local Testing

To test locally before deploying:

```bash
cd frontend

# Create .env file with your MySQL details:
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=yoga

python run.py
```

Then test at `http://localhost:5000`

---

## After Setup

Once database is working:
- All users are stored in `users` table
- Pose history is tracked in `user_pose_history`
- Recommendations are saved in `user_recommendations`
- Everything should work without "Internal Server Error"

**Questions?** Check the error logs on Render for specific database errors and error messages.
