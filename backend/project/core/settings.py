from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url

load_dotenv()

# ----------------------------------------------------
# BASE DIRECTORY
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# SECURITY / DEPLOYMENT
# ----------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

# Render will set ALLOWED_HOSTS using env var
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    os.getenv("RENDER_EXTERNAL_HOSTNAME", ""),
    "electricity-backend.onrender.com",
]


# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://electricity-backend.onrender.com",
    "https://electricity-frontend.netlify.app",
]

# ----------------------------------------------------
# INSTALLED APPS
# ----------------------------------------------------
INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "app",
]

# ----------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# ----------------------------------------------------
# TEMPLATES (Backend Only — frontend deployed separately)
# ----------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [], 
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ----------------------------------------------------
# DATABASE (SQLite for local + Postgres on Render)
# ----------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ----------------------------------------------------
# STATIC FILES + WHITENOISE
# ----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------------------------------
# DEFAULT FIELD
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------------------------
# CORS
# ----------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://electricity-frontend.netlify.app",
]

CORS_ALLOW_CREDENTIALS = True

# ----------------------------------------------------
# REST FRAMEWORK + JWT
# ----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
