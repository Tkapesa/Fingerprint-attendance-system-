"""
============================================================
USER VIEWS - STUDENT REGISTRATION
============================================================
Handles student registration and profile management.
============================================================
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Course


def student_registration(request):
    """
    Student Registration View.
    
    Process:
    1. Student fills registration form (full name, email, student ID, course code, password)
    2. System creates User account
    3. System creates UserProfile
    4. Redirect to fingerprint enrollment
    
    URL: /register/
    Method: GET (show form), POST (process registration)
    """
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        course_code = request.POST.get('course_code')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, '❌ Passwords do not match!')
            return render(request, 'users/registration.html', {'courses': Course.objects.all()})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ Email already registered!')
            return render(request, 'users/registration.html', {'courses': Course.objects.all()})
        
        # Check if student ID already exists
        if UserProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, '❌ Student ID already registered!')
            return render(request, 'users/registration.html', {'courses': Course.objects.all()})
        
        # Check if course exists (case-insensitive search)
        try:
            course = Course.objects.get(course_code__iexact=course_code)
        except Course.DoesNotExist:
            messages.error(request, f'❌ Course code "{course_code}" not found!')
            return render(request, 'users/registration.html', {'courses': Course.objects.all()})
        
        try:
            # Create User account (username = student_id for uniqueness)
            user = User.objects.create_user(
                username=student_id,  # Use student ID as username
                email=email,
                password=password,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            
            # Create UserProfile
            profile = UserProfile.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                student_id=student_id,
                course=course,
                role='student',
                fingerprint_enrolled=False
            )
            
            # Auto-login the user
            login(request, user)
            
            messages.success(request, f'✅ Registration successful! Welcome {full_name}!')
            messages.info(request, '👆 Please enroll your fingerprint to complete registration.')
            
            # Redirect to fingerprint enrollment
            return redirect('enroll_own_fingerprint')
            
        except Exception as e:
            messages.error(request, f'❌ Registration failed: {str(e)}')
            return render(request, 'users/registration.html', {'courses': Course.objects.all()})
    
    # GET request - show registration form
    courses = Course.objects.all()
    return render(request, 'users/registration.html', {'courses': courses})


def user_login(request):
    """
    Student Login View.
    
    Students can login with student ID and password.
    Used for: viewing profile, re-enrolling fingerprint
    
    Note: For attendance, students just scan fingerprint (no login needed)
    
    URL: /login/
    """
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        # Authenticate user (username is student_id)
        user = authenticate(request, username=student_id, password=password)
        
        if user is not None:
            login(request, user)
            
            try:
                profile = UserProfile.objects.get(user=user)
                messages.success(request, f'✅ Welcome back, {profile.full_name}!')
                
                # Redirect based on role
                if profile.role == 'instructor':
                    return redirect('instructor_dashboard')
                else:
                    return redirect('home')
                    
            except UserProfile.DoesNotExist:
                messages.warning(request, '⚠️ Profile not found. Please contact admin.')
                return redirect('home')
        else:
            messages.error(request, '❌ Invalid student ID or password!')
    
    return render(request, 'users/login.html')


@login_required
def user_logout(request):
    """
    Logout View.
    
    URL: /logout/
    """
    logout(request)
    messages.success(request, '👋 You have been logged out successfully.')
    return redirect('home')


@login_required
def student_profile(request):
    """
    Student Profile View.
    
    Shows student information and attendance history.
    
    URL: /profile/
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        # Get student's attendance logs
        from attendance.models import AttendanceLog
        attendance_logs = AttendanceLog.objects.filter(user=request.user).order_by('-timestamp')[:20]
        
        context = {
            'profile': profile,
            'attendance_logs': attendance_logs
        }
        return render(request, 'users/profile.html', context)
        
    except UserProfile.DoesNotExist:
        messages.error(request, '❌ Profile not found!')
        return redirect('home')

