"""
============================================================
ATTENDANCE LOG MODEL
============================================================
Records every attendance event with timestamp, course, and student details.
============================================================
"""
from django.db import models
from django.contrib.auth.models import User
from users.models import Course

class AttendanceLog(models.Model):
    """
    Attendance record for each student check-in.
    
    Fields:
        user: Which user's attendance is being logged
        student_name: Student's full name (denormalized for quick access)
        student_id: Student ID (denormalized for quick access)
        course: Which course the attendance is for
        timestamp: When attendance was marked (auto-set)
        date: Date of attendance (auto-set from timestamp)
        time: Time of attendance (auto-set from timestamp)
        status: Present or Absent
        scan_method: How attendance was marked (fingerprint/manual)
    
    Purpose: 
        - Track who attended and when
        - Generate attendance reports by course
        - Monitor attendance patterns
    """
    
    # Status options
    STATUS_CHOICES = (
        ('present', 'Present'),  # Successfully scanned fingerprint
        ('absent', 'Absent'),    # Manual absence marking
    )
    
    # Scan method options
    SCAN_METHOD_CHOICES = (
        ('fingerprint', 'Fingerprint Scan'),
        ('manual', 'Manual Entry'),
    )
    
    # User whose attendance is being logged
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Denormalized fields for quick access (stored from UserProfile)
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=50)
    
    # Course for this attendance
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name='attendance_logs'
    )
    
    # When attendance was marked (automatically set on creation)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Date and time separated for easier filtering
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    # Attendance status (present/absent)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    
    # How was attendance marked
    scan_method = models.CharField(max_length=20, choices=SCAN_METHOD_CHOICES, default='fingerprint')

    def __str__(self):
        """String representation of attendance record"""
        return f"{self.student_name} ({self.student_id}) - {self.course.course_code} - {self.date} {self.time}"
    
    class Meta:
        """Metadata for the model"""
        ordering = ['-timestamp']  # Most recent first
        verbose_name = "Attendance Log"
        verbose_name_plural = "Attendance Logs"
        # Prevent duplicate attendance for same student, course, and date
        unique_together = ['user', 'course', 'date']


