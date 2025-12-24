"""
============================================================
USERS URL CONFIGURATION
============================================================
URL routes for user registration, login, logout, profile.
============================================================
"""
from django.urls import path
from . import views

urlpatterns = [
    # Student registration
    path('register/', views.student_registration, name='student_registration'),
    
    # Login page
    path('login/', views.user_login, name='user_login'),
    
    # Logout
    path('logout/', views.user_logout, name='user_logout'),
    
    # Student profile
    path('profile/', views.student_profile, name='student_profile'),
]
