import os

os.environ.setdefault('SECRET_KEY', 'test-only-key-never-for-deployment')
os.environ.setdefault('USE_SQLITE', 'true')
from .settings import *  # noqa: F403,E402

DEBUG = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
