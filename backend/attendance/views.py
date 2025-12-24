"""
============================================================
ATTENDANCE VIEWS
============================================================
Handles instructor dashboard and attendance viewing.
============================================================
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AttendanceLog
from users.models import UserProfile, Course
from datetime import date, timedelta


@login_required
def instructor_dashboard(request):
    """
    Instructor Dashboard - View courses and attendance.
    
    Access: Instructors and admins only
    URL: /attendance/dashboard/
    
    Features:
        - View all courses instructor is teaching
        - Select course to view attendance
        - Quick stats for each course
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
    
    # Get courses for this instructor
    if request.user.is_staff:
        # Admins can see all courses
        courses = Course.objects.all()
    else:
        # Instructors see only their courses
        courses = Course.objects.filter(instructor=request.user)
    
    # Get attendance stats for each course (today)
    today = date.today()
    course_stats = []
    
    for course in courses:
        total_students = UserProfile.objects.filter(course=course, role='student').count()
        present_today = AttendanceLog.objects.filter(course=course, date=today).count()
        
        course_stats.append({
            'course': course,
            'total_students': total_students,
            'present_today': present_today,
            'absent_today': total_students - present_today
        })
    
    context = {
        'course_stats': course_stats,
        'today': today
    }
    
    return render(request, 'attendance/instructor_dashboard.html', context)


@login_required
def course_attendance(request, course_code):
    """
    View attendance for a specific course.
    
    Access: Instructors and admins only
    URL: /attendance/course/<course_code>/
    
    Features:
        - View all students in the course
        - See who attended today
        - Filter by date
        - Search students
    """
    # Check if user is instructor or admin
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'instructor' and not request.user.is_staff:
            messages.error(request, '❌ Access denied!')
            return redirect('home')
    except UserProfile.DoesNotExist:
        if not request.user.is_staff:
            messages.error(request, '❌ Access denied!')
            return redirect('home')
    
    # Get the course
    try:
        course = Course.objects.get(course_code=course_code.upper())
    except Course.DoesNotExist:
        messages.error(request, f'❌ Course "{course_code}" not found!')
        return redirect('instructor_dashboard')
    
    # Check if instructor has access to this course
    if not request.user.is_staff and course.instructor != request.user:
        messages.error(request, '❌ You do not have access to this course!')
        return redirect('instructor_dashboard')
    
    # Get date filter from query params (default to today)
    selected_date = request.GET.get('date', str(date.today()))
    try:
        selected_date = date.fromisoformat(selected_date)
    except:
        selected_date = date.today()
    
    # Get all students in this course
    students = UserProfile.objects.filter(course=course, role='student').order_by('full_name')
    
    # Get attendance logs for selected date
    attendance_logs = AttendanceLog.objects.filter(
        course=course,
        date=selected_date
    ).order_by('time')
    
    # Create attendance summary
    attended_student_ids = set(log.student_id for log in attendance_logs)
    
    student_attendance = []
    for student in students:
        attended = student.student_id in attended_student_ids
        attendance_time = None
        
        if attended:
            log = attendance_logs.filter(student_id=student.student_id).first()
            if log:
                attendance_time = log.time
        
        student_attendance.append({
            'student': student,
            'attended': attended,
            'time': attendance_time
        })
    
    # Stats
    total_students = students.count()
    present_count = len(attended_student_ids)
    absent_count = total_students - present_count
    
    context = {
        'course': course,
        'selected_date': selected_date,
        'student_attendance': student_attendance,
        'attendance_logs': attendance_logs,
        'total_students': total_students,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_percentage': round((present_count / total_students * 100) if total_students > 0 else 0, 1)
    }
    
    return render(request, 'attendance/course_attendance.html', context)


@login_required
def attendance_report(request, course_code):
    """
    Download attendance report for a course (Excel).
    
    Access: Instructors and admins only
    URL: /attendance/report/<course_code>/
    """
    from django.http import HttpResponse
    import pandas as pd
    from datetime import datetime
    
    # Check access
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'instructor' and not request.user.is_staff:
            messages.error(request, '❌ Access denied!')
            return redirect('home')
    except UserProfile.DoesNotExist:
        if not request.user.is_staff:
            messages.error(request, '❌ Access denied!')
            return redirect('home')
    
    # Get the course
    try:
        course = Course.objects.get(course_code=course_code.upper())
    except Course.DoesNotExist:
        messages.error(request, f'❌ Course "{course_code}" not found!')
        return redirect('instructor_dashboard')
    
    # Get all attendance logs for this course
    logs = AttendanceLog.objects.filter(course=course).order_by('-date', 'time')
    
    # Convert to DataFrame
    data = [
        {
            'Student ID': log.student_id,
            'Student Name': log.student_name,
            'Date': log.date.strftime('%Y-%m-%d'),
            'Time': log.time.strftime('%I:%M %p'),
            'Status': log.status.capitalize(),
            'Scan Method': log.scan_method.capitalize(),
        }
        for log in logs
    ]
    
    df = pd.DataFrame(data)
    
    if df.empty:
        df = pd.DataFrame(columns=[
            'Student ID', 'Student Name', 'Date', 'Time', 'Status', 'Scan Method'
        ])
    
    # Generate filename
    filename = f'attendance_{course_code}_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    
    # Create HTTP response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    
    # Write to Excel
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response


