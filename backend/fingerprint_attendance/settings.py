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
# Using Firebase Realtime Database for app data
# SQLite database for Django's internal tables (sessions, admin, migrations)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# ========== FIREBASE CONFIGURATION ==========
# Firebase Firestore Database Configuration
# Get these credentials from Firebase Console: https://console.firebase.google.com
# 1. Create a project
# 2. Go to Project Settings > Service Accounts
# 3. Generate new private key (JSON file)
# 4. Place the JSON file in the project root and update FIREBASE_CREDENTIALS_PATH

import os

# Path to Firebase service account credentials JSON file
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')

# Firebase Project ID
FIREBASE_PROJECT_ID = 'attendance-system-31683'

# Firebase Web API Key (for ESP32 and Frontend)
# Get from: Firebase Console > Project Settings > General > Web API Key
FIREBASE_API_KEY = 'AIzaSyCJoIAWWbPXB5EHEAcXj_epzRCElh1BCgU'

# Firebase configuration dictionary (for web apps, ESP32, and Frontend onSnapshot)
FIREBASE_CONFIG = {
    'apiKey': 'AIzaSyCJoIAWWbPXB5EHEAcXj_epzRCElh1BCgU',
    'authDomain': 'attendance-system-31683.firebaseapp.com',
    'projectId': 'attendance-system-31683',
    'storageBucket': 'attendance-system-31683.firebasestorage.app',
    'messagingSenderId': '859845763144',
    'appId': '1:859845763144:web:cfe51da2090756dbb4b87d',
    'measurementId': 'G-3ML5456HKL'
}

# Firestore Database Name (default is '(default)')
FIRESTORE_DATABASE = '(default)'

