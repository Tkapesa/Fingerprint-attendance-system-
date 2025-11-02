"""
============================================================
MAIN URL CONFIGURATION
============================================================
This file routes URLs to the appropriate views in the application.

URL Structure:
- /                          -> Home page
- /register/                 -> Student registration
- /login/                    -> Login page
- /logout/                   -> Logout
- /profile/                  -> Student profile
- /admin/                    -> Django admin panel
- /fingerprint/scan/         -> Scan fingerprint for attendance (NO LOGIN)
- /fingerprint/enroll-own/   -> Student enrolls own fingerprint
- /fingerprint/enroll/       -> Instructor enrolls student fingerprint
- /attendance/dashboard/     -> Instructor dashboard
- /attendance/course/<code>/ -> View course attendance
- /attendance/report/<code>/ -> Download attendance report
- /reports/generate/         -> Download all attendance data
============================================================
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Home page - main dashboard
    path('', views.home, name='home'),
    
    # Django admin interface - for managing users and data
    path('admin/', admin.site.urls),
    
    # User authentication and registration
    path('', include('users.urls')),
    
    # Fingerprint module - enrollment and scanning
    path('fingerprint/', include('fingerprint.urls')),
    
    # Attendance module - instructor dashboard and viewing
    path('attendance/', include('attendance.urls')),
    
    # Reports module - generate and download reports
    path('reports/', include('reports.urls')),
]


