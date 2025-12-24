"""
Project-level views
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    """Home page - redirects to authentication landing page"""
    return redirect('landing_page')

def about(request):
    """About page"""
    return HttpResponse("""
    <h1>About Fingerprint Attendance System</h1>
    <p>This system uses fingerprint authentication for attendance tracking.</p>
    <p><a href="/">← Back to Home</a></p>
    """)

def contact(request):
    """Contact page"""
    return HttpResponse("""
    <h1>Contact Support</h1>
    <p>For support, please contact your system administrator.</p>
    <p><a href="/">← Back to Home</a></p>
    """)