"""
============================================================
REPORTS URL CONFIGURATION
============================================================
URL routes for report generation (kept for backward compatibility).
Note: Reports are now primarily accessed through instructor dashboard.
============================================================
"""
from django.urls import path
from . import views

urlpatterns = [
    # Generate and download Excel attendance report (all data)
    path('generate/', views.generate_report, name='generate_report'),
]

 