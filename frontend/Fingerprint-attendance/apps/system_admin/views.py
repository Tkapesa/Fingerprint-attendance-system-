from django.shortcuts import render, redirect
from django.contrib import messages

def admin_dashboard(request):
    user_name = request.session.get('user_name', 'Admin')
    context = {
        'message': f'Welcome {user_name}!',
    }
    return render(request, 'system_admin/admin_dashboard.html', context)

def update_user_role(request, user_id):
    if request.method == 'POST':
        new_role = request.POST.get('role', '').strip()
        # Logic to update role in DB goes here
        messages.success(request, f"Role for user {user_id} updated to {new_role}.")
        return redirect('system_admin:admin_dashboard')
    
    context = {
        'user_id': user_id,
    }
    return render(request, 'system_admin/update_role.html', context)

def enroll_fingerprint(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        # Logic to start fingerprint enrollment goes here
        messages.success(request, f"Enrollment started for student {student_id}.")
        return redirect('system_admin:admin_dashboard')
    
    context = {}
    return render(request, 'system_admin/enroll_fingerprint.html', context)
