"""
============================================================
FINGERPRINT VIEWS
============================================================
Handles fingerprint enrollment and scanning functionality.

Key Functions:
- enroll_own_fingerprint: Students enroll their own fingerprint after registration
- enroll_fingerprint: Admins/instructors enroll fingerprints for students
- scan_fingerprint: Students scan to mark attendance (NO LOGIN REQUIRED)
============================================================
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from users.models import UserProfile
from .models import FingerprintScan
from attendance.models import AttendanceLog
from .r307 import R307


@login_required
def enroll_own_fingerprint(request):
    """
    Student enrolls their own fingerprint (after registration).
    
    Process:
    1. Student is already logged in (just registered)
    2. Student places finger on R307 sensor
    3. Sensor captures and stores template
    4. Template saved to student's profile
    5. Student can now use fingerprint for attendance
    
    URL: /fingerprint/enroll-own/
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Initialize fingerprint sensor
            r307 = R307()
            
            # Capture fingerprint template
            template = r307.enroll_fingerprint()
            r307.close()
            
            if template:
                # Save template to user profile
                profile.fingerprint_template = template
                profile.fingerprint_enrolled = True
                profile.save()
                
                messages.success(request, f'✅ Fingerprint enrolled successfully!')
                messages.success(request, '🎉 Registration complete! You can now mark attendance by scanning your fingerprint.')
                return redirect('home')
            else:
                messages.error(request, '❌ Error: Could not connect to fingerprint sensor.')
        
        # Display enrollment page
        return render(request, 'fingerprint/enroll_own.html', {'profile': profile})
        
    except UserProfile.DoesNotExist:
        messages.error(request, '❌ Profile not found!')
        return redirect('home')


@login_required
def enroll_fingerprint(request):
    """
    Enroll a fingerprint for any student (Admin/Instructor only).
    
    Process:
    1. Admin/instructor enters student ID
    2. Student places finger on R307 sensor
    3. Sensor captures and stores template
    4. Template saved to student's profile
    
    Access: Admin/Instructor users only
    URL: /fingerprint/enroll/
    """
    # Check if user is instructor or admin
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'instructor' and not request.user.is_staff:
            messages.error(request, '❌ Access denied! Only instructors can access this page.')
            return redirect('home')
    except UserProfile.DoesNotExist:
        if not request.user.is_staff:
            messages.error(request, '❌ Access denied!')
            return redirect('home')
    
    if request.method == 'POST':
        # Get student ID from form
        student_id = request.POST.get('student_id')
        
        try:
            # Find student profile by student ID
            student_profile = UserProfile.objects.get(student_id=student_id)
            
            # Initialize fingerprint sensor
            r307 = R307()
            
            # Capture fingerprint template
            template = r307.enroll_fingerprint()
            r307.close()
            
            if template:
                # Save template to student profile
                student_profile.fingerprint_template = template
                student_profile.fingerprint_enrolled = True
                student_profile.save()
                
                messages.success(request, f'✅ Fingerprint enrolled for {student_profile.full_name} ({student_id})!')
                return redirect('enroll_fingerprint')
            else:
                messages.error(request, '❌ Error: Could not connect to fingerprint sensor.')
                
        except UserProfile.DoesNotExist:
            messages.error(request, f'❌ Student ID "{student_id}" not found!')
    
    # Display enrollment form with list of students
    students = UserProfile.objects.filter(role='student').order_by('full_name')
    return render(request, 'fingerprint/enroll.html', {'students': students})


def scan_fingerprint(request):
    """
    Scan fingerprint for attendance marking (NO LOGIN REQUIRED).
    
    Process:
    1. Student places finger on R307 sensor
    2. Sensor captures fingerprint
    3. System matches against ALL enrolled fingerprints
    4. If match found: Log attendance with timestamp, date, time, course
    5. If no match: Show error and allow retry
    
    Access: Public - NO authentication required
    URL: /fingerprint/scan/
    
    This is the main attendance marking endpoint!
    """
    if request.method == 'POST':
        # Initialize fingerprint sensor
        r307 = R307()
        
        # Scan fingerprint
        scan = r307.scan_fingerprint()
        r307.close()
        
        if not scan:
            messages.error(request, '❌ Error: Could not connect to fingerprint sensor.')
            return render(request, 'fingerprint/scan.html')
        
        # Try to match against ALL enrolled fingerprints
        all_profiles = UserProfile.objects.filter(fingerprint_enrolled=True, role='student')
        
        matched_profile = None
        for profile in all_profiles:
            if profile.fingerprint_template:
                # Simple comparison (in production, use R307's match function)
                if r307.match_fingerprint(profile.fingerprint_template, scan):
                    matched_profile = profile
                    break
        
        if matched_profile:
            # SUCCESS: Fingerprint matched!
            
            # Check if student has a course
            if not matched_profile.course:
                messages.error(request, f'⚠️ {matched_profile.full_name}: No course assigned. Please contact administrator.')
                return render(request, 'fingerprint/scan.html')
            
            # Check if already marked attendance today for this course
            from datetime import date
            today = date.today()
            
            existing_attendance = AttendanceLog.objects.filter(
                user=matched_profile.user,
                course=matched_profile.course,
                date=today
            ).first()
            
            if existing_attendance:
                messages.warning(request, f'⚠️ {matched_profile.full_name}: Attendance already marked today for {matched_profile.course.course_code} at {existing_attendance.time.strftime("%I:%M %p")}')
            else:
                # Create new attendance log
                AttendanceLog.objects.create(
                    user=matched_profile.user,
                    student_name=matched_profile.full_name,
                    student_id=matched_profile.student_id,
                    course=matched_profile.course,
                    status='present',
                    scan_method='fingerprint'
                )
                
                messages.success(request, f'✅ Welcome {matched_profile.full_name}!')
                messages.success(request, f'📚 Attendance marked for {matched_profile.course.course_code} - {matched_profile.course.course_name}')
            
            # Save scan record for audit trail
            FingerprintScan.objects.create(
                user=matched_profile.user,
                scan_data=scan
            )
            
        else:
            # FAILED: Fingerprint not recognized
            messages.error(request, '❌ Fingerprint not recognized!')
            messages.info(request, '💡 Please ensure your finger is clean and properly placed on the sensor.')
            messages.info(request, '💡 If problem persists, contact your instructor.')
    
    # Display scan page
    return render(request, 'fingerprint/scan.html')


