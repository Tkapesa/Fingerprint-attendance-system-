"""
============================================================
MAIN APPLICATION VIEWS
============================================================
Views for the main application pages.
============================================================
"""
from django.shortcuts import render

def home(request):
    """
    Home page view - displays the main dashboard with links to all features.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered home.html template
    """
    return render(request, 'home.html')
 