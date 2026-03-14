# Render Deployment Troubleshooting

## Issue: No Images Showing on Render

**Solution:** The app now gracefully handles missing pose images by showing placeholders. Pose descriptions and guides still display correctly.

- If you have pose images in a `data/` folder locally, they won't be stored on Render (git ignores them)
- Instead, placeholders are shown with full pose guides from `dataset/pose_guides.json`
- To add images to Render, upload them to a persistent storage service or include them in git

## Issue: Webcam Not Initializing

**Causes & Solutions:**

1. **Browser Permissions**
   - Allow camera access when prompted
   - Check browser settings: Settings → Privacy → Camera
   - Ensure app is accessed via HTTPS (Render provides this)

2. **HTTPS Required**
   - `navigator.mediaDevices.getUserMedia()` requires HTTPS in production
   - Render automatically provides HTTPS for free tier apps ✓

3. **Silent Failures**
   - Check browser console (F12 → Console tab) for errors
   - Status will show: "Error: Could not access webcam"

4. **Network/CDN Issues**
   - MediaPipe loads from CDN: `https://cdn.jsdelivr.net/npm/@mediapipe/pose/`
   - Check if CDN is accessible from your region
   - Fallback: error message displays "MediaPipe Pose library not loaded"

## Issue: Image Upload Fails

**Solution:** Check these settings in your `.env`:

```ini
SAVED_IMAGES_DIR=/tmp/yoga_uploads  # Render's /tmp is ephemeral but sufficient for uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png
```

## Testing Locally

Before deploying, run locally:

```bash
cd Align-AI-Yoga
python test_flows.py  # Tests all routes locally
```

## Verifying on Render

1. Log in with test account
2. Go to **Yoga** → **Step 1** → See beginner poses with guide
3. Select mood → See recommendations with guide text
4. Click **Analyze** → Select pose → Test webcam button
5. If webcam prompts: **Allow** camera access
6. Check console (F12) for any errors

## Known Limitations

- Pose image data folder not included (large files)
- Webcam requires browser permission grant
- MediaPipe CDN required for live analysis
- Render free tier: 50 hours/month, restarts frequently

## Dashboard Issue

If Dashboard shows no history after upload:

1. Check browser console for SQL errors
2. Verify database connection: `SQLITE_DB_PATH` env var is set
3. Render persists SQLite in `/var/data/` (check `Procfile` for path)

