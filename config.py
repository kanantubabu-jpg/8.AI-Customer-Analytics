"""
Application configuration for AI Customer Analytics Platform.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration with secure defaults."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Set DATABASE_URL for MySQL; defaults to SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'ai_customer_analytics.db')}",
    )
    # MySQL example: mysql+pymysql://root:password@localhost/ai_customer_analytics
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "dataset", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    DATASET_DIR = os.path.join(BASE_DIR, "dataset")
