# System Architecture

This document explains the design decisions and architecture of Align AI Yoga.

## Overview

Align AI Yoga follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│         User Interface (HTML/CSS/JS)    │
├─────────────────────────────────────────┤
│           Flask Routes Layer            │
│  (auth.py, yoga.py, dashboard.py)       │
├─────────────────────────────────────────┤
│         Service Layer                   │
│  (pose_service, recommendation_service) │
├─────────────────────────────────────────┤
│         ML/Computation Layer            │
│  (MediaPipe, angle_calculator, etc.)    │
├─────────────────────────────────────────┤
│         Database Layer (SQLite)         │
└─────────────────────────────────────────┘
```

## Layer Breakdown

### 1. Routes Layer (`app/routes/`)

**Responsibility**: HTTP request/response handling, form validation, redirects

**Files**:
- `auth.py` - Registration, login, logout
- `yoga.py` - Mood selection, pose analysis, recommendations
- `dashboard.py` - History, chatbot

**Key Principle**: Routes are **thin** — they parse input and delegate to services.

```python
# Good: Route delegates to service
@yoga_bp.route("/analyze", methods=["POST"])
def analyze():
    result = analyze_pose(image_path, pose_name)
    return render_template("results.html", data=result)
```

### 2. Service Layer (`app/services/`)

**Responsibility**: Business logic, ML orchestration, database coordination

**Files**:
- `pose_service.py` - Orchestrates ML pipeline (detect → calculate → evaluate)
- `recommendation_service.py` - Lazy-loads SVD recommender singleton
- `pose_guide_service.py` - Loads pose metadata and instructions
- `chat_service.py` - Chatbot interactions

**Key Principle**: Services are **testable** — pure functions with no Flask dependencies.

```python
# In service: pure logic, no Flask context
def analyze_pose(image_path: str, pose_name: str) -> Dict:
    keypoints = extract_keypoints(image_path)
    angles = compute_body_angles(keypoints)
    evaluation = evaluate_pose(angles, pose_name)
    feedback = build_pose_feedback(evaluation)
    return feedback
```

### 3. ML Layer (`frontend/ml/`)

**Responsibility**: Computer vision, math, ML algorithms

**Modules**:
- `pose_detector.py` - MediaPipe 33-point landmark extraction
- `angle_calculator.py` - Joint angle computation (pure math)
- `pose_evaluator.py` - Compare detected angles vs reference
- `pose_corrector.py` - Generate user-friendly corrections
- `pose_feedback.py` - Format feedback for UI
- `recommender.py` - SVD-based recommendation engine
- `reference_angles.py` - Reference pose angle database
- `evaluation_config.py` - Severity thresholds, scoring rules

**Key Principle**: No Flask or web framework dependencies. Pure computations.

```python
# Pure math: no side effects, easy to test
def calculate_angle(a, b, c) -> float:
    """Vector angle at vertex B."""
    # Uses numpy, returns float
```

### 4. Database Layer (`app/utils/db.py`)

**Responsibility**: SQL execution, connection management

**Design**:
- **Per-Request Pattern**: New connection created per request, closed in teardown hook
- **Both SQLite & MySQL**: Supports switching via `DB_TYPE` env var
- **Parameterized Queries**: All queries use `?` placeholders to prevent SQL injection
- **Placeholder Conversion**: Automatically converts MySQL `%s` to SQLite `?`

```python
# Database layer: handles conversion
def execute(query: str, values: tuple):
    if db_type == 'sqlite':
        query = query.replace('%s', '?')
    cursor.execute(query, values)  # Safe
```

## Data Flow Example: Pose Analysis

```
1. User uploads image
   └─> upload_image_form() [route]

2. Route calls service
   └─> analyze_pose(image_path, pose_name) [service]

3. Service calls ML modules in sequence
   ├─> extract_keypoints(image) → 33 landmarks
   ├─> compute_body_angles(keypoints) → dict of angles
   ├─> evaluate_pose(angles, pose_name) → scores + feedback
   └─> build_pose_feedback(evaluation) → formatted output

4. Service saves to database
   └─> execute("INSERT INTO yoga_sessions ...") [db layer]

5. Route renders result
   └─> render_template("results.html", feedback=output) [route]

6. User sees annotated image + corrections
   └─> Image served from static/saved_images/
```

## Design Patterns Used

### 1. Service Layer / Dependency Inversion
- Routes don't import ML directly
- Services coordinate between routes and ML
- Testable: services are just functions

### 2. Lazy Loading
- MediaPipe loaded on first pose detection request (saves startup time)
- Recommender built once, cached for app lifetime
- Reduces cold-start time on Render

### 3. Configuration via Environment
- All secrets/paths in `config.py`
- Loaded from `.env`
- Easy to switch between dev/prod (SQLite vs MySQL)

### 4. Per-Request Database Connections
- Flask `g` object stores connection
- Teardown hook closes after request
- Prevents connection leaks and stale connections

### 5. Template Inheritance
- `index.html` as base template
- All pages extend it (navbar, footer consistent)
- Easy to update site-wide styling

## Performance Optimizations

### 1. Lazy MediaPipe Loading
```python
# Only imported when first used
def _get_mediapipe_pose():
    if _MP_POSE is None:
        import mediapipe as mp
        _MP_POSE = mp.solutions.pose
    return _MP_POSE
```

### 2. SVD Recommender Caching
```python
# Built once at app startup, reused
_recommender = None

def get_recommender():
    global _recommender
    if _recommender is None:
        _recommender = YogaRecommender(csv_path)
    return _recommender
```

### 3. Static File Serving
- Images stored as file paths, not BLOBs
- Flask/Nginx serve directly (much faster than Python)

### 4. Database Connection Pooling
- Not implemented (single-process Render free tier)
- Could add with scaling

## Security Architecture

### Authentication
- **Passwords**: Werkzeug PBKDF2-SHA256 (salted, iterated)
- **Sessions**: Flask secure cookies (signed, not encrypted)
- **Decorators**: `@login_required` protects endpoints

### Data Protection
- **SQL Injection**: Parameterized queries everywhere
- **Secrets**: Never in code, always in `.env` (not committed)
- **File Uploads**: Secure filename sanitization
- **CORS**: Per-route (login only, no external API)

## Scalability Path

### Current (Free Tier)
- Single Render instance (512 MB RAM)
- SQLite database (local)
- Single-threaded Gunicorn

### Next Steps (Paid Tier)
1. **Multi-process**: `gunicorn -w 4` with multiple workers
2. **PostgreSQL**: Scale database (Render Postgres, $7/mo)
3. **Redis**: Cache recommendations, image processing results
4. **Async Tasks**: Celery for long-running ML jobs
5. **CDN**: Cloudflare for static assets
6. **Load Balancer**: Multiple app instances

## Testing Strategy

### Unit Tests (`tests/`)
- Test ML modules in isolation
- Test database layer with fixtures
- Test services with mock dependencies

### Integration Tests
- Test routes with Flask test client
- Full request-response cycle

### Manual Testing
- Use `Makefile` commands: `make test`
- Check coverage: `pytest --cov=app`

## Future Architecture

### Planned Improvements
- **Queue System**: Render background jobs for long ML operations
- **API Versioning**: `/api/v1/` endpoints for mobile apps
- **WebSockets**: Real-time feedback during live analysis
- **Database Sharding**: If user base scales
- **Microservices**: Separate ML inference service (GPU-accelerated)

---

**Designed for simplicity, maintainability, and scalability.** 🚀
