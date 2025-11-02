"""
============================================================
FINGERPRINT ATTENDANCE SYSTEM - SETTINGS
============================================================
This file contains all configuration settings for the 
fingerprint-based attendance tracking system.

Project: Fingerprint Attendance System
Purpose: Track attendance using R307 fingerprint sensor
Author: [Your Company Name]
Date: November 2025
============================================================
"""

from pathlib import Path

# ========== PROJECT DIRECTORY SETUP ==========
# Base directory - root folder of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent


# ========== SECURITY SETTINGS ==========
# WARNING: Change this secret key in production!
# Generate a new one using: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'django-insecure-x41!imqlti1ct08k(_12jo^rwy5kt_wmp$ai+qq7goar5aw=%n'

# Debug mode - MUST be False in production for security
DEBUG = True

# Allowed hosts - add your domain/IP in production (e.g., ['yourdomain.com', '192.168.1.100'])
ALLOWED_HOSTS = []


# ========== INSTALLED APPLICATIONS ==========
# These are the apps that make up our fingerprint attendance system
INSTALLED_APPS = [
    # Django built-in apps (required)
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # User authentication
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session management
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static files (CSS, JavaScript, Images)
    
    # Custom apps for attendance system
    'users',        # User profile management
    'fingerprint',  # Fingerprint enrollment and scanning
    'attendance',   # Attendance logging
    'reports',      # Report generation (Excel exports)
]


# ========== MIDDLEWARE CONFIGURATION ==========
# Middleware processes requests/responses (security, sessions, auth, etc.)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware', # Session handling
    'django.middleware.common.CommonMiddleware',           # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',    # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# ========== URL CONFIGURATION ==========
# Main URL configuration file
ROOT_URLCONF = 'fingerprint_attendance.urls'

# ========== TEMPLATES CONFIGURATION ==========
# Template engine settings for rendering HTML pages
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,  # Look for templates in each app's 'templates' folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ========== WSGI APPLICATION ==========
# WSGI application for deployment
WSGI_APPLICATION = 'fingerprint_attendance.wsgi.application'


# ========== DATABASE CONFIGURATION ==========
# Using SQLite for simplicity - easy to deploy and maintain
# For production with many users, consider PostgreSQL or MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file location
    }
}


# ========== PASSWORD VALIDATION ==========
# Password security validators to ensure strong passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ========== INTERNATIONALIZATION ==========
# Language and timezone settings
LANGUAGE_CODE = 'en-us'  # English (United States)

# IMPORTANT: Set this to your local timezone for accurate attendance timestamps
# Examples: 'America/New_York', 'Europe/London', 'Asia/Kolkata', 'UTC'
TIME_ZONE = 'UTC'

USE_I18N = True  # Enable internationalization

USE_TZ = True    # Use timezone-aware datetimes


# ========== STATIC FILES ==========
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# ========== DEFAULT SETTINGS ==========
# Default primary key field type for models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== LOGIN/LOGOUT REDIRECTS ==========
# Redirect users to home page after login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/admin/login/'  # Use Django admin login page

