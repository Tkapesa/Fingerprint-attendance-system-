"""
============================================================
FINGERPRINT URL CONFIGURATION
============================================================
URL routes for fingerprint-related pages.
============================================================
"""
from django.urls import path
from . import views

urlpatterns = [
    # Student enrolls own fingerprint (after registration)
    path('enroll-own/', views.enroll_own_fingerprint, name='enroll_own_fingerprint'),
    
    # Instructor/admin enrolls fingerprint for any student
    path('enroll/', views.enroll_fingerprint, name='enroll_fingerprint'),
    
    # Fingerprint scanning for attendance (NO LOGIN REQUIRED)
    path('scan/', views.scan_fingerprint, name='scan_fingerprint'),
]

 