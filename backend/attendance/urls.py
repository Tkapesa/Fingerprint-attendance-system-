"""
============================================================
ATTENDANCE URL CONFIGURATION
============================================================
URL routes for instructor dashboard and attendance viewing.
============================================================
"""
from django.urls import path
from . import views

urlpatterns = [
    # Instructor dashboard - view all courses
    path('dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    
    # View attendance for specific course
    path('course/<str:course_code>/', views.course_attendance, name='course_attendance'),
    
    # Download attendance report for course (Excel)
    path('report/<str:course_code>/', views.attendance_report, name='attendance_report'),
]

 