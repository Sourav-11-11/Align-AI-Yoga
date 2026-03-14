# Render Deployment Troubleshooting

## Issue: Placeholder Images Instead of Pose Photos

**Why This Happens:**
- Pose images in `frontend/data/` are .gitignored (too large for git)
- Render doesn't have these images, so placeholders show instead
- **This is expected behavior** - descriptions still show perfectly

**Solution Options:**

1. **Use Placeholders (Current - Recommended)**
   - All pose descriptions display from `pose_guides.json`
   - Placeholders are styled consistently
   - Lightweight and fast
   - ✅ Best for free tier Render deployment

2. **Upload Images Manually to Render**
   - SSH into Render service
   - Upload pose image folders to `/var/data/frontend/data/`
   - Persist across restarts via Render settings
   - Note: Requires restart after upload

3. **Host Images on CDN**
   - Upload to AWS S3, Cloudinary, or similar
   - Update `POSES_DIR` config to CDN URL
   - Images download on demand

## Issue: Webcam Not Initializing

**Symptoms:** Button shows "Initializing webcam..." forever

**Causes & Solutions:**

### 1. Browser Permissions
- [ ] Allow camera access when prompted
- [ ] Check Settings → Privacy → Camera  
- [ ] Ensure HTTPS (Render provides this automatically)

### 2. MediaPipe CDN
- Loads from `https://cdn.jsdelivr.net/npm/@mediapipe/pose/`
- If blocked by network: won't load
- Check browser console (F12 → Console)

### 3. Render Service Issue
If you see server error with "Could not import mediapipe pose":
- This means MediaPipe failed during deployment
- **Fix:** Restart Render service or redeploy
- Check `runtime.txt` has `python-3.11.7`

## Issue: Image Upload Fails

**Error:** `{"error":"Server Error","message":"Could not import mediapipe pose..."}`

**Solutions:**

1. **Restart Render**
   - Render dashboard → Manual → Restart
   - Wait 2 minutes, try again

2. **Redeploy Latest**
   - `git push origin main`
   - Render auto-deploys
   - View build logs for status

3. **Check Python Version**
   - Verify `runtime.txt` contains: `python-3.11.7`
   - Redeploy if changed

## Issue: Dashboard Shows No History

**If uploads aren't saved:**

1. Check SQLite path
   - Should persist to `/var/data/` on Render
   - Automatic across restarts

2. Test locally
   - `cd frontend && python run.py`
   - Upload an image
   - Verify Dashboard shows it

3. Check schema
   - Tables auto-created: `users`, `yoga_sessions`
   - Auto-migrations on startup

## Quick Verification Checklist

- [ ] Home page loads (register → login → logout)
- [ ] Yoga page shows 3 beginner poses + descriptions
- [ ] Select mood → see 3 recommendations + guides
- [ ] Analyze page → pose selector appears
- [ ] Camera permission prompt appears (allow or deny)
- [ ] Image upload processes (error or success)
- [ ] Dashboard shows session history
- [ ] Chatbot responds

## Testing on Render

**Test Account:**
```
Email: demo@example.com
Password: demo123
```

**Test Steps:**
1. Register new account
2. Go Yoga → See beginner poses (placeholders + descriptions)
3. Select mood → Get recommendations with guides
4. Click Analyze → Try webcam (or skip/upload image)
5. Check Dashboard for sessions
6. Test Chatbot

## MediaPipe Troubleshooting

MediaPipe 0.10.32 requires Python 3.11 on Linux (Render's OS).

**If MediaPipe import fails:**

1. **First try:** Restart Render service
   - Render dashboard → Manual → Restart
   - This usually resolves transient issues

2. **Then try:** Redeploy code
   - `git commit --allow-empty -m "redeploy"`
   - `git push origin main`
   - Wait for build to complete

3. **Alternative:** Use lightweight MediaPipe
   - Update `requirements.txt`
   - Change `mediapipe>=0.10.30` to `mediapipe-lite`
   - Redeploy

## Advanced: Check Render Logs

1. Render dashboard → Logs
2. Look for during deploy:
   - `Successfully installed mediapipe-0.10.32`
   - `Running 'python frontend/run.py'`
3. Look for during errors:
   - `Could not import mediapipe`
   - `ImportError` or `ModuleNotFoundError`

## Known Limits

- Free tier: 50 compute hours/month
- Spin-down after 15 min inactivity (cold start ~30s)
- SQLite persists in `/var/data/`
- Images are ephemeral in `/tmp/`
- No webcam on server (browser-side only)

