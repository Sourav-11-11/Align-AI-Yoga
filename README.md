# CSP Align AI — Yoga Pose Recognition & Recommendation System

> An AI-powered yoga guidance platform: real-time pose correction via computer vision, mood-based pose recommendations via collaborative filtering, and session tracking — built as a portfolio-grade ML web project.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Demo Flow](#demo-flow)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [ML Design Decisions](#ml-design-decisions)
- [Installation & Setup](#installation--setup)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Running Tests](#running-tests)
- [Codebase Audit & Improvements](#codebase-audit--improvements)
- [Portfolio Notes](#portfolio-notes)
- [Future Enhancements](#future-enhancements)

---

## 📌 Overview

**CSP Align AI** is a yoga guidance web application that combines computer vision, machine learning, and a Flask backend to deliver two core capabilities:

1. **Pose Correction** — the user uploads a photo of themselves performing a yoga pose. MediaPipe detects 33 body landmarks, the system calculates four joint angles (shoulder, elbow, hip, knee), compares them to calibrated reference values, and returns specific, actionable feedback (e.g., *"Increase your Hip Angle by 14.3°"*).

2. **Mood-Based Recommendations** — before practising, the user selects their current mood. An SVD-based collaborative filtering model (trained on a mood↔pose interaction dataset) recommends the top 3 poses most suited to that mood.

User sessions, feedback, and pose images are persisted to MySQL and surfaced in a personal dashboard.

---

## ✨ Features

### 1. **User Authentication**
   - User registration with email validation
   - Secure login system
   - Session management
   - Password confirmation

### 2. **Mood-Based Pose Recommendation**
   - Users select their current mood
   - ML model recommends top 3 yoga poses
   - Collaborative filtering algorithm using SVD (Singular Value Decomposition)
   - Dataset-driven recommendations from user behavior patterns

### 3. **Real-Time Pose Correction**
   - Upload yoga pose images
   - Automatic keypoint detection using MediaPipe
   - Joint angle calculation (Shoulder, Elbow, Hip, Knee)
   - Comparison with reference angles
   - Dynamic correction suggestions (e.g., "Increase shoulder angle by 15°")
   - Annotated image output with detected keypoints and angles

### 4. **User Dashboard**
   - View complete session history
   - Filter sessions by date range
   - Track mood evolution and poses practiced
   - View corrected images and feedback
   - Monitor progress over time

### 5. **Interactive ChatBot**
   - Yoga-related Q&A
   - User engagement interface

### 6. **Comprehensive Pose Library**
   - 70+ yoga poses with reference data
   - Each pose has calibrated angle values for:
     - Shoulder Angle
     - Elbow Angle
     - Hip Angle
     - Knee Angle

---

## 🛠️ Tech Stack

### **Frontend**
| Technology | Purpose |
|-----------|---------|
| **Flask** | Web framework & routing |
| **HTML5** | Page structure & templates |
| **CSS3** | Styling & responsive design |
| **JavaScript** | Client-side interactivity |
| **Jinja2** | Template engine |

### **Backend & ML/AI**
| Technology | Purpose |
|-----------|---------|
| **Python 3.x** | Core programming language |
| **TensorFlow** | Deep learning framework |
| **MediaPipe** | Pose estimation & keypoint detection |
| **OpenCV (cv2)** | Image processing & annotation |
| **PoseNet** | Pre-trained pose detection model |
| **NumPy** | Numerical computations |
| **Pandas** | Data manipulation & analysis |
| **SciPy** | SVD & sparse matrix operations |
| **scikit-learn** | Collaborative filtering utilities |
| **Pillow (PIL)** | Image handling |
| **joblib** | Model serialization |

### **Database**
| Component | Purpose |
|-----------|---------|
| **MySQL** | Relational database |
| **Tables** | users, dashboard, sessions |

### **Libraries & Dependencies**
```
flask
flask-mail
mysql-connector-python
tensorflow
tensorflow-hub
mediapipe
opencv-python
numpy
pandas
scipy
scikit-learn
pillow
joblib
werkzeug
```

---

## 🏗️ Architecture

```
CSP Align AI Yoga System
│
├── Frontend Layer (Flask + HTML/CSS/JS)
│   ├── User Authentication
│   ├── Mood Selection Interface
│   ├── Image Upload Interface
│   ├── Feedback Display
│   └── Dashboard
│
├── AI/ML Processing Layer
│   ├── MediaPipe Pose Estimator
│   ├── Angle Calculator
│   ├── Correction Suggestion Engine
│   └── SVD-based Recommender
│
├── Database Layer (MySQL)
│   ├── User Management
│   ├── Session History
│   └── Dashboard Records
│
└── Data Layer
    ├── Reference Pose Angles (JSON)
    ├── Recommendation Dataset (CSV)
    ├── Model Weights (YOLOv3, YOLOv8)
    └── Training Data (70+ Yoga Poses)
```

---

## 📁 Project Structure

```
CODE/
│
├── FRONT END/
│   ├── app.py                    # Main Flask application with all routes
│   ├── test.py                   # Testing & experimentation
│   ├── __pycache__/              # Python cache
│   │
│   ├── data/                     # Yoga pose images (70+ folders)
│   │   ├── adho mukha svanasana/
│   │   ├── bakasana/
│   │   ├── virabhadrasana i/
│   │   └── ... (60+ more poses)
│   │
│   ├── dataset/                  # Data files
│   │   ├── Recommendation_yoga_data.csv      # Mood-pose recommendations
│   │   ├── reference_poses_keypoints.json    # Reference angle data
│   │   ├── yolov3.cfg                        # YOLOv3 config
│   │   ├── yolov3.weights                    # YOLOv3 weights
│   │   └── yolov8n.pt                        # YOLOv8 nano weights
│   │
│   ├── static/
│   │   ├── css/                  # Stylesheets
│   │   ├── js/                   # JavaScript files
│   │   ├── images/               # Static images
│   │   ├── img/                  # Temporary pose images
│   │   └── saved_images/         # Annotated output images
│   │
│   └── templates/                # HTML templates
│       ├── index.html            # Home page
│       ├── login.html            # Login page
│       ├── register.html         # Registration page
│       ├── home.html             # Dashboard home
│       ├── yoga1.html            # Mood selection
│       ├── yoga2.html            # Pose display & image upload
│       ├── yoga3.html            # Correction feedback
│       ├── dashboard.html        # User history dashboard
│       ├── chatbot.html          # Chatbot interface
│       └── about.html            # About page
│
└── BACK END/
    ├── final.ipynb               # Main data processing notebook
    ├── rec.ipynb                 # Recommendation system notebook
    ├── temp_data.ipynb           # Temporary data experiments
    ├── test.py                   # Testing script
    ├── Recommendation_yoga_data.csv        # Source recommendation data
    └── reference_poses_keypoints.json      # Reference data
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8+**
- **MySQL Server** (running on localhost:3306)
- **pip** (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd "d:\sourav\NEW LAPPY IMP FILES\CSP ALIGN AI YOGA PROJECT WEB DEV\CODE"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-mail mysql-connector-python tensorflow tensorflow-hub mediapipe opencv-python numpy pandas scipy scikit-learn pillow joblib werkzeug
```

### Step 4: Set Up MySQL Database
```sql
CREATE DATABASE yoga;
USE yoga;

-- Create users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Create dashboard table
CREATE TABLE dashboard (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100),
    email VARCHAR(100),
    mood_name VARCHAR(50),
    yoga_name VARCHAR(100),
    uploaded_img LONGBLOB,
    corrected_img LONGBLOB,
    feedback TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES users(email)
);
```

### Step 5: Configure Flask App
Edit `FRONT END/app.py` - Modify MySQL connection settings:
```python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",          # Your MySQL username
    password="",          # Your MySQL password
    port="3306",
    database='yoga'
)
```

### Step 6: Run the Application
```bash
cd "FRONT END"
python app.py
```

The application will start at `http://localhost:5000`

---

## 💡 Usage Guide

### **Step 1: Register/Login**
1. Visit `http://localhost:5000`
2. Click "Register" to create a new account
3. Enter name, email, and password
4. Click "Login" to sign in

### **Step 2: Get Pose Recommendations**
1. After login, click "Start Yoga"
2. Select your current mood from dropdown
3. System recommends top 3 yoga poses
4. Click on a pose to practice it

### **Step 3: Upload & Get Correction**
1. Select a recommended yoga pose
2. Click "Upload Image" to upload your pose
3. AI analyzes your pose and detects keypoints
4. System displays:
   - Annotated image with skeleton overlay
   - Joint angles (Shoulder, Elbow, Hip, Knee)
   - Specific correction suggestions
5. Example feedback: "Increase shoulder angle by 15°"

### **Step 4: View Dashboard**
1. Click "Dashboard" in navigation
2. View all your past sessions
3. Filter by date range
4. See mood progression and poses practiced
5. View feedback history

### **Step 5: Interact with ChatBot**
1. Visit ChatBot section
2. Ask yoga-related questions
3. Get answers and recommendations

---

## 🧠 How It Works

### **1. Mood-Based Recommendation Engine**

#### Algorithm: Collaborative Filtering (Matrix Factorization via SVD)

```
Step 1: Load recommendation dataset
        (Historical mood → yoga pose pairings)

Step 2: Build interaction matrix
        Rows = Moods (Happy, Stressed, Tired, etc.)
        Columns = Yoga Poses
        Values = Frequency of pairing

Step 3: Apply Singular Value Decomposition (SVD)
        Reduce matrix to latent features (k=num_features)
        Extract: U (mood features), Σ (strength), V^T (pose features)

Step 4: For new user with mood M:
        - Get mood index in matrix
        - Compute mood latent vector: U[M] × Σ
        - Calculate scores: mood_vector × V^T
        - Return top 3 poses with highest scores

Benefits:
- Personalized recommendations
- Handles sparse data well
- Fast predictions
- Scalable
```

### **2. Pose Detection & Correction System**

#### Technology: MediaPipe Pose Estimation

```
Step 1: Image Input
        User uploads yoga pose image

Step 2: Pose Landmark Detection
        MediaPipe detects 33 body landmarks:
        - Nose, eyes, ears
        - Shoulders, elbows, wrists, hands
        - Hips, knees, ankles, feet
        - Spine points

Step 3: Keypoint Extraction
        Extract 6 key joints:
        - Left Shoulder, Left Elbow, Left Wrist
        - Left Hip, Left Knee, Left Ankle

Step 4: Angle Calculation
        Calculate 4 joint angles using law of cosines:
        - Shoulder Angle = angle(elbow-shoulder-hip)
        - Elbow Angle = angle(wrist-elbow-shoulder)
        - Hip Angle = angle(shoulder-hip-knee)
        - Knee Angle = angle(hip-knee-ankle)

Step 5: Reference Comparison
        Fetch reference angles for detected pose:
        - Load from POSES_REFERENCE_ANGLES dictionary
        - Has 70+ poses with calibrated angles

Step 6: Correction Generation
        For each joint:
        - If detected_angle < reference_angle - 5°:
          → "Increase {joint} angle by {difference}°"
        - If detected_angle > reference_angle + 5°:
          → "Decrease {joint} angle by {difference}°"
        - Otherwise: "{joint} angle is correct"

Step 7: Image Annotation
        Draw on image:
        - Green dots for joint positions
        - Blue lines connecting joints
        - White text showing angles
        - Save annotated image to static/saved_images/

Step 8: Feedback Display
        Show user:
        - Original uploaded image
        - Annotated image with skeleton
        - Specific correction suggestions
```

### **3. Database Flow**

```
User Registration:
Register → Validate email unique → Hash password → Store in users table

User Login:
Email & Password → Validate against users table → Create session

Session Recording:
After correction → Extract: user_id, mood, pose, images, feedback
→ Encode images to BLOB
→ Insert into dashboard table
→ Associate with user email & timestamp

Dashboard View:
Logged-in user → Query dashboard table WHERE email = session_email
→ Fetch user's complete history
→ Decode images from BLOB
→ Display with filtering options
```

---

## 🗄️ Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
```

| Field | Type | Constraints |
|-------|------|-------------|
| id | INT | Primary Key, Auto Increment |
| name | VARCHAR(100) | Not Null |
| email | VARCHAR(100) | Unique, Not Null |
| password | VARCHAR(100) | Not Null |

### **Dashboard Table**
```sql
CREATE TABLE dashboard (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100),
    email VARCHAR(100),
    mood_name VARCHAR(50),
    yoga_name VARCHAR(100),
    uploaded_img LONGBLOB,
    corrected_img LONGBLOB,
    feedback TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES users(email)
);
```

| Field | Type | Purpose |
|-------|------|---------|
| id | INT | Primary Key |
| user_name | VARCHAR(100) | User's name |
| email | VARCHAR(100) | FK to users |
| mood_name | VARCHAR(50) | Selected mood |
| yoga_name | VARCHAR(100) | Yoga pose name |
| uploaded_img | LONGBLOB | Original image |
| corrected_img | LONGBLOB | Annotated image |
| feedback | TEXT | Correction suggestions |
| date | DATETIME | Session timestamp |

---

## 🔑 Key Components

### **1. Reference Pose Angles Dictionary**
Located in `FRONT END/app.py` - Contains 70+ yoga poses with calibrated joint angles:

```python
POSES_REFERENCE_ANGLES = {
    "adho mukha svanasana": {
        "Shoulder Angle": 179,
        "Elbow Angle": 170,
        "Hip Angle": 161,
        "Knee Angle": 157
    },
    "bakasana": {
        "Shoulder Angle": 96,
        "Elbow Angle": 108,
        "Hip Angle": 123,
        "Knee Angle": 90
    },
    # ... 68+ more poses
}
```

### **2. Angle Calculation Function**
Uses Law of Cosines to compute angles from 3D body points:

```python
def calculate_angle(a, b, c):
    """
    Calculate angle at point b using points a and c
    Input: 3D coordinates [x, y, z]
    Output: Angle in degrees
    """
    a = np.array(a)
    b = np.array(b)  # Vertex point
    c = np.array(c)
    
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)
```

### **3. Correction Suggestion Engine**
Generates personalized feedback based on angle differences:

```python
def provide_correction_suggestion(detected_angles, reference_angles):
    corrections = []
    for joint, detected_angle in detected_angles.items():
        reference_angle = reference_angles.get(joint)
        angle_diff = detected_angle - reference_angle
        
        if angle_diff < -5:
            corrections.append(f"Increase {joint} angle by {abs(angle_diff):.2f}°")
        elif angle_diff > 5:
            corrections.append(f"Decrease {joint} angle by {abs(angle_diff):.2f}°")
        else:
            corrections.append(f"{joint} angle is correct.")
    return corrections
```

### **4. Recommendation Engine**
SVD-based collaborative filtering:

```python
# Build interaction matrix
interaction_matrix = csr_matrix((len(moods), len(poses)))
for _, row in df.iterrows():
    mood_idx = mood_to_idx[row['Mood Before']]
    pose_idx = pose_to_idx[row['Yoga Practice']]
    interaction_matrix[mood_idx, pose_idx] += 1

# Matrix factorization
u, sigma, vt = svds(interaction_matrix, k=num_features)

# Recommendation
def recommend_poses(mood, u, sigma, vt, top_n=3):
    mood_idx = mood_to_idx[mood]
    mood_latent_features = np.dot(u[mood_idx, :], sigma)
    pose_scores = np.dot(mood_latent_features, vt)
    top_pose_indices = np.argsort(pose_scores)[::-1][:top_n]
    return [poses[idx] for idx in top_pose_indices]
```

---

## 🌐 API Routes

| Route | Method | Purpose | Parameters |
|-------|--------|---------|-----------|
| `/` | GET | Home page | - |
| `/about` | GET | About page | - |
| `/register` | GET, POST | User registration | name, email, password, c_password |
| `/login` | GET, POST | User login | email, password |
| `/home` | GET | Dashboard home | - |
| `/yoga1` | GET, POST | Mood selection | mood |
| `/yoga2` | GET, POST | Pose display & upload | pose_name, mood, img |
| `/yoga3` | GET | Correction feedback | - |
| `/dashboard` | GET, POST | User history | frm_date, to_date (optional) |
| `/chatbot` | GET | ChatBot interface | - |

---

## 📊 Data Flow Diagram

```
User Input (Mood)
    ↓
Recommendation Engine (SVD)
    ↓
Top 3 Poses Suggested
    ↓
User Selects Pose & Uploads Image
    ↓
MediaPipe Landmark Detection
    ↓
Keypoint Extraction (6 joints)
    ↓
Angle Calculation (4 angles)
    ↓
Reference Angle Lookup
    ↓
Comparison & Feedback Generation
    ↓
Image Annotation with Keypoints
    ↓
Display Feedback & Annotated Image
    ↓
Save Session to Database
    ↓
Dashboard Update
```

---

## 🎯 Supported Yoga Poses (70+)

### Categories:
- **Standing Poses**: Virabhadrasana I/II/III, Utthita Trikonasana, Vriksasana
- **Forward Bends**: Prasarita Padottanasana, Janu Sirsasana, Paschimottanasana
- **Backbends**: Dhanurasana, Urdhva Mukhasana, Kapotasana
- **Twists**: Ardha Matsyendrasana, Parivrtta Parsvakonasana
- **Arm Balances**: Bakasana, Parsva Bakasana, Mayurasana
- **Inversions**: Salamba Sirsasana, Salamba Sarvangasana
- **Sitting Poses**: Sukhasana, Gomukhasana, Baddha Konasana
- **Supine Poses**: Savasana, Supta Virasana, Ananda Balasana
- **And 40+ more specialized poses**

---

## 🚀 Future Enhancements

### Short Term
- [ ] Mobile app version (React Native / Flutter)
- [ ] Real-time webcam feed support
- [ ] Pose video analysis
- [ ] Multi-pose angle comparison
- [ ] Email session reports

### Medium Term
- [ ] Advanced ChatBot with NLP
- [ ] Progress tracking graphs
- [ ] Difficulty level progression
- [ ] Multi-language support
- [ ] Offline mode capability

### Long Term
- [ ] Social sharing features
- [ ] Community challenges
- [ ] Personalized workout plans
- [ ] Integration with fitness trackers
- [ ] AR-based virtual instructor
- [ ] Advanced ML models (3D pose estimation)
- [ ] Emotional recognition from webcam
- [ ] Payment gateway integration

---

## 📝 Configuration Notes

### **TensorFlow Hub Models**
- **PoseNet Model**: `https://tfhub.dev/google/movenet/singlepose/lightning/4`
- **Downloads automatically** on first run
- **Requires internet connection** for first execution

### **MediaPipe Models**
- **Pose Estimation**: Runs locally after download
- **Model Complexity**: 2 (Full model with high accuracy)
- **Detection Confidence**: 0.5 (50% threshold for landmark detection)

### **Image Processing**
- **Input Size**: 192×192 pixels (for PoseNet)
- **Detection Size**: Variable (OpenCV handles resizing)
- **Output Format**: PNG with annotated keypoints
- **Storage**: `static/saved_images/` directory

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: MySQL Connection Error
```
Solution: Ensure MySQL is running on localhost:3306
Check credentials in app.py (default: root user, no password)
Run: mysql -u root -p
```

**Issue**: TensorFlow Model Download Fails
```
Solution: Check internet connection
Clear TensorFlow cache: rm -rf ~/.cache/tensorflow
Re-run application to re-download model
```

**Issue**: MediaPipe Pose Not Detected
```
Solution: Ensure image has clear body visibility
Try different angles or lighting
Use high-resolution images (min 192×192)
```

**Issue**: Port 5000 Already in Use
```
Solution: Change port in app.py:
app.run(debug=True, port=5001)
```

---

## 📚 References & Resources

- **MediaPipe Documentation**: https://mediapipe.dev/
- **TensorFlow Hub**: https://tfhub.dev/
- **OpenCV Documentation**: https://docs.opencv.org/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **SciPy SVD Documentation**: https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.svds.html

---

## 📄 License

This project is created for educational purposes. All datasets and models are used for research and learning.

---

## 👨‍💻 Developer Info

**Project**: CSP Align AI - Yoga Pose Recognition & Recommendation
**Domain**: Computer Vision + Machine Learning + Web Development
**Year**: 2026

---

## 🤝 Contributing

For bug reports, feature requests, or improvements, please document:
1. Issue description
2. Steps to reproduce
3. Expected vs actual behavior
4. System configuration

---

## ✅ Verification Checklist

Before deployment/sharing, ensure:
- [ ] MySQL database is created and configured
- [ ] All Python dependencies installed
- [ ] Flask app runs without errors on `localhost:5000`
- [ ] User registration and login working
- [ ] Mood-based recommendations functioning
- [ ] Image upload and pose detection active
- [ ] Dashboard displaying user history
- [ ] All database queries executing properly
- [ ] Images saving to `static/saved_images/`
- [ ] ChatBot interface accessible

---

**Happy Yoga! 🧘‍♀️🧘‍♂️**

For any questions or issues, refer to the troubleshooting section or check the backend logs in the console.
