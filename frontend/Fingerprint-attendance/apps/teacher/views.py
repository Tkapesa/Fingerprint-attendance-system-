from django.shortcuts import render, redirect
from django.contrib import messages

def get_teacher_name(request):
    return request.session.get('user_name', 'Demo Teacher')

def teacher_dashboard(request):
    context = {
        'teacher_name': get_teacher_name(request),
        'active_courses': 3,
        'total_students': 85,
        'today_attendance': 78,
        'active_sessions': 2,
        'active_sessions_list': [
            {
                'course_name': 'Computer Science 101',
                'course_code': 'CS101',
                'students_present': 35,
                'total_students': 40,
                'start_time': '10:00 AM',
                'duration': 60
            },
            {
                'course_name': 'Database Systems',
                'course_code': 'CS201',
                'students_present': 28,
                'total_students': 32,
                'start_time': '2:00 PM',
                'duration': 90
            }
        ],
        'recent_activity': [
            {
                'type': 'attendance',
                'title': 'Attendance Marked',
                'description': 'Attendance marked for CS101',
                'time': '10:15 AM'
            },
            {
                'type': 'session',
                'title': 'Session Created',
                'description': 'New session created for Database Systems',
                'time': '9:30 AM'
            },
            {
                'type': 'student',
                'title': 'Student Added',
                'description': 'New student Emma Johnson enrolled',
                'time': 'Yesterday, 4:20 PM'
            }
        ]
    }
    return render(request, 'teacher/dashboard.html', context)

def create_session(request):
    courses = [
        {'id': 'cs101', 'code': 'CS101', 'name': 'Computer Science 101', 'student_count': 40},
        {'id': 'cs201', 'code': 'CS201', 'name': 'Database Systems', 'student_count': 32},
        {'id': 'cs301', 'code': 'CS301', 'name': 'Data Structures', 'student_count': 28},
        {'id': 'cs401', 'code': 'CS401', 'name': 'Algorithms', 'student_count': 25},
    ]

    if request.method == 'POST':
        session_name = request.POST.get('session_name', '').strip()
        course_id = request.POST.get('course_id', '').strip()
        duration = request.POST.get('duration', '60')

        if not session_name:
            messages.error(request, "Please enter a session name.")
            return redirect('teacher:create_session')

        if not course_id:
            messages.error(request, "Please select a course.")
            return redirect('teacher:create_session')

        selected_course = next((c for c in courses if c['id'] == course_id), None)
        messages.success(request, f"✅ Session '{session_name}' created for {selected_course['name']}.")
        messages.info(request, "📱 QR code generated. Students can scan to mark attendance.")
        return redirect('teacher:teacher_dashboard')

    context = {'teacher_name': get_teacher_name(request), 'courses': courses}
    return render(request, 'teacher/create_session.html', context)

def view_session(request, session_id):
    session_data = {
        'id': session_id,
        'name': 'CS101 - Lecture 5',
        'course_code': 'CS101',
        'course_name': 'Computer Science 101',
        'status': 'active',
        'start_time': '10:00 AM',
        'duration': 60,
        'students_present': 35,
        'total_students': 40,
        'attendance_rate': 87.5
    }

    attendance_records = [
        {'student_name': 'John Smith', 'student_id': 'ST001', 'time': '10:05 AM', 'method': 'fingerprint'},
        {'student_name': 'Emma Johnson', 'student_id': 'ST002', 'time': '10:07 AM', 'method': 'fingerprint'},
        {'student_name': 'Michael Brown', 'student_id': 'ST003', 'time': '10:10 AM', 'method': 'QR code'},
    ]

    context = {'session': session_data, 'attendance_records': attendance_records, 'teacher_name': get_teacher_name(request)}
    return render(request, 'teacher/view_session.html', context)

def end_session(request, session_id):
    messages.success(request, f"Session {session_id} ended successfully.")
    return redirect('teacher:teacher_dashboard')

def attendance_reports(request):
    context = {
        'teacher_name': get_teacher_name(request),
        'reports': [
            {'course': 'CS101', 'date': '2024-01-15', 'present': 35, 'absent': 5, 'rate': 87.5},
            {'course': 'CS201', 'date': '2024-01-15', 'present': 28, 'absent': 4, 'rate': 87.5},
            {'course': 'CS101', 'date': '2024-01-14', 'present': 38, 'absent': 2, 'rate': 95.0},
        ]
    }
    return render(request, 'teacher/reports.html', context)

def manage_students(request):
    context = {
        'teacher_name': get_teacher_name(request),
        'courses': [
            {
                'code': 'CS101',
                'name': 'Computer Science 101',
                'students': [
                    {'id': 'ST001', 'name': 'John Smith', 'email': 'john@example.com'},
                    {'id': 'ST002', 'name': 'Emma Johnson', 'email': 'emma@example.com'},
                    {'id': 'ST003', 'name': 'Michael Brown', 'email': 'michael@example.com'},
                ]
            },
            {
                'code': 'CS201',
                'name': 'Database Systems',
                'students': [
                    {'id': 'ST004', 'name': 'Sarah Davis', 'email': 'sarah@example.com'},
                    {'id': 'ST005', 'name': 'Robert Wilson', 'email': 'robert@example.com'},
                ]
            }
        ]
    }
    return render(request, 'teacher/manage_students.html', context)
