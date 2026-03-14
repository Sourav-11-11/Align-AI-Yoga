# 🧘 Align AI Yoga — Demo Guide

This guide walks you through the key features of Align AI Yoga. Try it yourself!

---

## 🚀 Quick Start

### Local Demo (2 minutes)

```bash
# 1. Clone & install
git clone https://github.com/Sourav-11-11/Align-AI-Yoga.git
cd Align-AI-Yoga
pip install -r requirements.txt

# 2. Run app
cd frontend
python run.py

# 3. Open browser
# Visit http://localhost:5000
```

### Demo Account (No Registration Required)

| Email | Password |
|-------|----------|
| demo@example.com | demo123 |

Or create your own account via the **Register** button.

---

## ✨ Features to Try

### 1. **User Authentication** (30 seconds)
- [ ] Click **"Register"** and create an account
- [ ] Log out (**Logout** button in navbar)
- [ ] Log back in with your credentials
- ✅ **What to notice**: Secure password hashing, session management, clean error messages

### 2. **Mood-Based Pose Recommendations** (1 minute)
- [ ] After login, click **"Start Yoga Session"**
- [ ] Select a mood (Energetic, Calm, Focused, etc.)
- [ ] View 3 AI-recommended poses based on your mood
- ✅ **What to notice**: 
  - SmartML algorithm personalizes recommendations
  - Each pose shows reference image and instructions
  - Difficulty levels displayed

### 3. **Real-Time Pose Analysis (Live)** (2 minutes)
- [ ] Click **"Analyze"** → **"Live Analysis"**
- [ ] Allow camera permission
- [ ] Perform one of the recommended poses
- [ ] See real-time joint corrections overlay
- ✅ **What to notice**:
  - MediaPipe detects 33 body landmarks in real-time
  - Joint angles shown on-screen
  - Green = correct, Yellow = off, Red = needs adjustment
  - Instant feedback for each joint

### 4. **Image Upload Analysis** (2 minutes)
- [ ] Click **"Analyze"** → **"Image Upload"**
- [ ] Upload a yoga pose photo (or use a phone screenshot)
- [ ] Get detailed corrections for that pose
- [ ] See accuracy score and specific joint feedback
- ✅ **What to notice**:
  - Works with any yoga pose from the library
  - Provides joint-by-joint corrections
  - Annotated image shows where joints are out of alignment

### 5. **Progress Dashboard** (1 minute)
- [ ] Click **"Dashboard"**
- [ ] View:
  - 📊 **Total Sessions**: Count of all practice sessions
  - 🔥 **Practice Streak**: Consecutive days practiced
  - 📜 **Session History**: Previously analyzed poses
  - 📸 Both original and corrected images stored
- [ ] Filter sessions by **date range**
- ✅ **What to notice**:
  - Clean data visualization
  - Quick stats at a glance
  - Easy session lookup

### 6. **AI Chatbot** (1 minute)
- [ ] Click **"Chatbot"** (bottom of navbar)
- [ ] Ask questions like:
  - "What's Chakrasana?"
  - "How to improve pose accuracy?"
  - "Recommend beginner poses"
- [ ] See AI-generated responses
- ✅ **What to notice**:
  - Context-aware chatbot
  - Helpful suggestions for next interaction

### 7. **Responsive Design** (Mobile Test)
- [ ] Open app on your phone
- [ ] Navigate through features
- [ ] Try Live Analysis on mobile (works great!)
- ✅ **What to notice**: Complete mobile experience, touch-friendly

---

## 🏗️ Technical Deep Dive (For Recruiters)

### Code Quality
- [ ] View [ARCHITECTURE.md](ARCHITECTURE.md) → Explains layered design
- [ ] View [app/routes/auth.py](frontend/app/routes/auth.py) → Clean authentication with logging
- [ ] View [app/services/pose_service.py](frontend/app/services/pose_service.py) → ML orchestration
- [ ] View [ml/pose_detector.py](frontend/ml/pose_detector.py) → Pure math, no dependencies

### Security Features
- [ ] Passwords: Werkzeug PBKDF2-SHA256 hashing ✅
- [ ] SQL Queries: Parameterized (prevents injection) ✅
- [ ] Sessions: Secure Flask cookies ✅
- [ ] Logging: Tracks auth events for audit ✅

### ML Pipeline
- **MediaPipe**: 33-point body pose detection
- **Angle Calculator**: Pure geometry (no ML overhead)
- **Pose Evaluator**: Compares vs reference angles
- **SVD Recommender**: Mood-based collaborative filtering

---

## 📊 Example Workflow

```
1. User logs in
   ↓
2. Selects mood (e.g., "Energetic")
   ↓
3. AI recommends 3 poses (SVD algorithm)
   ↓
4. User selects a pose
   ↓
5. Opens live camera OR uploads image
   ↓
6. MediaPipe extracts 33 body landmarks
   ↓
7. Angle calculator computes joint angles
   ↓
8. Pose evaluator scores vs reference
   ↓
9. Feedback generator creates corrections
   ↓
10. Results displayed with annotated image
    ↓
11. Session saved to SQLite database
    ↓
12. User views history in dashboard
```

---

## 🎯 Things Recruiters Should Notice

### Architecture
✅ **Layered Design**: Routes → Services → ML (clean separation)
✅ **No ML in Routes**: Pure HTTP handling
✅ **Reusable Services**: Easy to test, scale, maintain
✅ **Database Abstraction**: Supports SQLite + MySQL

### Code Quality
✅ **Docstrings**: Every function documented
✅ **Logging**: Debug, info, warning levels
✅ **Error Handling**: Try-catch with user messages
✅ **Type Hints**: Easy to understand intent

### DevOps
✅ **Docker Ready**: Can containerize
✅ **Render Deployment**: Free hosting verified
✅ **SQLite DB**: Zero external dependencies
✅ **Makefile Commands**: `make run-local`, `make test`

### Security
✅ **Password Hashing**: PBKDF2-SHA256 (salted, iterated)
✅ **SQL Injection Prevention**: Parameterized queries
✅ **Secrets Management**: .env files (not committed)
✅ **Session Security**: Flask secure cookies

---

## 🔧 Developer Testing (Optional)

### Run Tests
```bash
cd frontend
pytest tests/ -v
```

### Check Code Quality
```bash
flake8 frontend/app --max-line-length=100
```

### View Logs
```bash
# In development, watch the Flask console for log output
cd frontend
python run.py  # Watch console
```

---

## 📱 Test on Real Device

### Deploy to Render
1. Fork repository on GitHub
2. Go to [render.com](https://render.com)
3. Connect your GitHub repo
4. Deploy (takes ~3 minutes)
5. Share link with recruiters: `https://your-app.onrender.com`

---

## ❓ Common Questions

**Q: Does it actually detect poses?**  
A: Yes! MediaPipe is real-time computer vision. Try standing in a yoga pose during live analysis.

**Q: Can I use any yoga pose?**  
A: The app has 80+ poses in the library. Try any common yoga asana.

**Q: Is this production-ready?**  
A: Yes! It's deployed on Render with SQLite. Can scale to PostgreSQL + Redis for larger loads.

**Q: How did you get it free?**  
A: Render free tier + SQLite (no database service needed) = $0/month.

---

## 🎓 Learning Points

This project demonstrates:

1. **ML Integration**: MediaPipe for real-time pose detection
2. **Full-Stack Development**: Python backend + HTML/CSS frontend
3. **Database Design**: SQLite schema, parameterized queries
4. **System Architecture**: Layered design (routes → services → ml)
5. **Deployment**: Free hosting on Render
6. **Security**: Password hashing, SQL injection prevention
7. **DevOps**: Makefile, requirements.txt, .env management
8. **Professional Code**: Logging, docstrings, error handling

---

## 📸 Screenshots

*Coming soon: screenshots of key features*

---

**Enjoy the demo! 🧘‍♀️** 

Have questions? Check [architecture.md](ARCHITECTURE.md) or [README.md](README.md).
