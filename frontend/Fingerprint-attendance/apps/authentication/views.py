from django.shortcuts import render, redirect
from django.contrib import messages

def landing_page(request):
    return render(request, 'authentication/landing.html')


def login_student(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if email == 'student@example.com' and password == 'student123':
            request.session['user_role'] = 'student'
            request.session['user_email'] = email
            request.session['user_name'] = 'Student Demo'
            messages.success(request, "Student login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Try: student@example.com / student123")

    context = {
        'page_title': 'Student Login',
        'form_action': 'login_student'
    }
    return render(request, 'authentication/login_student.html', context)


def login_teacher(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if email == 'professor@example.edu' and password == 'teacher123':
            request.session['user_role'] = 'teacher'
            request.session['user_email'] = email
            request.session['user_name'] = 'Professor Demo'
            messages.success(request, "Teacher login successful!")
            return redirect('teacher:teacher_dashboard')
        else:
            messages.error(request, "Invalid credentials. Try: professor@example.edu / teacher123")

    context = {
        'page_title': 'Teacher Login',
        'form_action': 'login_teacher'
    }
    return render(request, 'authentication/login_teacher.html', context)


def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not email or not password:
            messages.error(request, "Please enter email and password")
            return redirect('login_admin')

        if email == 'admin@example.com' and password == 'admin123':
            request.session['user_role'] = 'admin'
            request.session['user_name'] = 'Administrator'
            messages.success(request, "Admin login successful!")
            return redirect('system_admin:admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'authentication/login_admin.html')


def register_teacher(request):
    context = {
        'page_title': 'Teacher Registration',
    }
    return render(request, 'authentication/register_teacher.html', context)


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('landing_page')
