from django.shortcuts import render

# Fingerprint scanning page
def scan_fingerprint(request):
    return render(request, 'attendance/scan.html')

# Attendance main dashboard
def dashboard(request):
    return render(request, 'attendance/dashboard.html')

# System admin page
def system_admin(request):
    return render(request, 'attendance/system_admin.html')

# Teacher dashboard page
def teacher_dashboard(request):
    return render(request, 'attendance/teacher.html')
