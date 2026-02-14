import os
from datetime import timedelta

class Config:
    # 🔑 Weak secret intentionally (FIRST in rockyou)
    SECRET_KEY = "chocolate"

    # Session security (except secret strength)
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # True لو HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Flask
    DEBUG = False
    TESTING = False
