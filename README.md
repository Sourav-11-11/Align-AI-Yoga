# 🧘 Align AI Yoga — AI-Powered Yoga Pose Analysis & Correction

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1+-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-red)
![MediaPipe](https://img.shields.io/badge/Vision-MediaPipe-yellow)

## Overview

**Align AI Yoga** is a full-stack web application that analyzes yoga poses in real-time using MediaPipe's computer vision. Users upload images or stream live video to receive instant form corrections, track progress, and get AI-powered pose recommendations based on mood and fitness level. The app features secure authentication, SQLite persistence, and is deployed free on Render.

---

## ✨ Features

- **Real-Time Pose Detection** — Analyzes yoga poses using 33-point body landmark detection
- **Intelligent Feedback** — Provides joint-by-joint corrections with actionable guidance
- **Progress Tracking** — Stores session history with accuracy scores and timestamps
- **Mood-Based Recommendations** — SVD-based collaborative filtering for personalized pose sequences
- **Multi-Mode Analysis** — Live webcam feed or static image upload
- **Secure Authentication** — Werkzeug PBKDF2-SHA256 password hashing, parameterized SQL queries
- **Responsive UI** — Works seamlessly on desktop, tablet, and mobile

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap |
| **Backend** | Python 3.11, Flask 3.1 |
| **Computer Vision** | MediaPipe 0.10.32 (pose detection) |
| **ML/Analytics** | scikit-learn (SVD recommendations), NumPy, pandas |
| **Database** | SQLite 3 (zero external dependencies) |
| **Server** | Gunicorn 21.2 |
| **Deployment** | Render (free tier) |

---

## 📸 Screenshots

*Add project screenshots here:*

- Dashboard with session history
- Live pose analysis interface
- Mood selection screen
- Pose correction feedback display

---

## 🚀 Installation (Local Setup)

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Align-AI-Yoga.git
cd Align-AI-Yoga

# 2. Install dependencies
pip install -r requirements.txt

# 3. Navigate to frontend and run
cd frontend
python run.py

# 4. Open browser
# Visit http://localhost:5000
```

---

## 🌐 Deployment (Render)

### Quick Deploy (5 minutes)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → Create New Web Service
3. Connect your GitHub repository
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `cd frontend && gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 60 wsgi:app`
6. Add **Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-random-string>
   DB_TYPE=sqlite
   ```
7. Deploy and you're live! ✅

For detailed instructions, see [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

## 🔐 Demo Login

| Field | Value |
|-------|-------|
| **Email** | demo@example.com |
| **Password** | demo123 |

*(Create your own account via registration)*

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── routes/          # auth.py, yoga.py, dashboard.py
│   ├── services/        # pose_service, recommendation_service, etc.
│   ├── utils/           # db.py (SQLite layer)
│   ├── ml/              # pose_detector, angle_calculator, pose_evaluator
│   ├── templates/       # HTML pages (11 templates)
│   ├── static/          # CSS, JS, images
│   └── config.py        # Configuration
├── dataset/             # Pose guides, reference angles
├── run.py               # Local development entry point
└── wsgi.py              # Production entry point

Procfile, requirements.txt, .env.example (root level)
```

---

## 🔄 How It Works

1. **User uploads image** or streams live video
2. **MediaPipe extracts** 33 body landmarks (joints, angles)
3. **Angle Calculator** computes joint angles from landmarks
4. **Pose Evaluator** compares against reference angles
5. **Feedback Generator** creates corrective guidance
6. **Annotator** highlights joints in original image
7. **Results displayed** with accuracy score and tips

---

## 🛠️ Development

### Run Tests
```bash
cd frontend
pytest tests/
```

### Local Database
SQLite automatically creates tables on first run. To reset:
```bash
rm frontend/align_yoga.db
```

---

## 🚀 Future Improvements

- [ ] Wearable integration (Apple Watch, Fitbit)
- [ ] Video tutorial library with pose breakdowns
- [ ] Social features (follow friends, share progress)
- [ ] Advanced ML model training on custom dataset
- [ ] Mobile app (React Native)

---

## 📝 License

MIT License — See LICENSE file for details

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push: `git push origin feature/YourFeature`
5. Open a Pull Request

---

## 💬 Questions?

Drop an issue on GitHub or reach out! Happy to help. 🧘‍♀️
