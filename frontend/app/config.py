"""
Application configuration.

All environment-specific settings live here, not scattered through the code.
Values are loaded from the .env file via python-dotenv.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-in-production")

    # ── Database ──────────────────────────────────────────────────────────────
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_NAME: str = os.getenv("DB_NAME", "yoga")

    # ── Paths ─────────────────────────────────────────────────────────────────
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_PATH: str = os.path.join(BASE_DIR, "dataset", "Recommendation_yoga_data.csv")
    POSE_GUIDES_PATH: str = os.path.join(BASE_DIR, "dataset", "pose_guides.json")
    POSES_DIR: str = os.path.join(BASE_DIR, "data")
    SAVED_IMAGES_DIR: str = os.path.join(BASE_DIR, "static", "saved_images")

    # ── ML Settings ───────────────────────────────────────────────────────────
    RECOMMENDATION_FACTORS: int = 10   # Number of latent factors for SVD
    TOP_POSES: int = 3                  # Number of poses to recommend
    POSE_DETECTION_CONFIDENCE: float = 0.5
    ANGLE_TOLERANCE: float = 5.0        # Degrees of tolerance before flagging a joint

    # ── AI Fallback ───────────────────────────────────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # ── File Upload ───────────────────────────────────────────────────────────
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024   # 16 MB upload limit
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg"}


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
