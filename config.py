"""
EduPredict - Application Configuration
Supports enterprise MySQL connectivity with automatic fallback to high-performance local SQLite
if a local MySQL daemon is not running during development or testing.
"""

import os
from dotenv import load_dotenv

# Load optional .env file
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_database_uri():
    """
    Determines database URI based on environment variables.
    Defaults directly to the local SQLite database (edupredict.db).
    """
    direct_url = os.getenv("DATABASE_URL")
    if direct_url:
        return direct_url

    use_mysql = os.getenv("USE_MYSQL", "false").lower()
    if use_mysql in ("true", "1", "yes"):
        mysql_host = os.getenv("MYSQL_HOST", "localhost")
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_pass = os.getenv("MYSQL_PASSWORD", "")
        mysql_db = os.getenv("MYSQL_DB", "edupredict_db")
        pwd_part = f":{mysql_pass}" if mysql_pass else ""
        return f"mysql+pymysql://{mysql_user}{pwd_part}@{mysql_host}:{mysql_port}/{mysql_db}"

    sqlite_path = os.path.join(BASE_DIR, "edupredict.db")
    return f"sqlite:///{sqlite_path}"

class Config:
    """Core application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "edupredict_purple_ai_secret_key_2026_secured")
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Brand Identity Colors
    BRAND = {
        "name": "EduPredict",
        "tagline": "Predict. Perform. Progress.",
        "primary_purple": "#7C3AED",
        "dark_purple": "#4C1D95",
        "background": "#F5F3FF",
        "accent_purple": "#A78BFA",
        "card_background": "#FFFFFF",
        "main_text": "#1E1B4B",
        "success_green": "#16A34A",
        "warning_orange": "#F59E0B",
        "danger_red": "#DC2626"
    }

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
