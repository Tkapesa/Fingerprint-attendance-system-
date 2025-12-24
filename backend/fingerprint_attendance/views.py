"""
============================================================
MAIN APPLICATION VIEWS
============================================================
Views for the main application pages.
============================================================
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    """
    Home page view.
    
    Args:
        request: HTTP request object
        
    Returns:
        Simple home page
    """
    return HttpResponse("Welcome to Fingerprint Attendance System. <a href='/static/realtime_dashboard.html'>Go to Dashboard</a>")
 