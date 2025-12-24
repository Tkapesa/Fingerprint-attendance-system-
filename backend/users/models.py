"""
============================================================
USER PROFILE MODEL
============================================================
Extended user model to store student/instructor information:
- Full student details (name, email, student ID, course)
- Fingerprint template data
- User role (Instructor or Student)
============================================================
"""
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Course Model - Represents courses in the system.
    
    Fields:
        course_code: Unique course identifier (e.g., "CS101", "MATH201")
        course_name: Full course name (e.g., "Introduction to Programming")
        instructor: Faculty member teaching the course
        description: Course description
        created_at: When course was created
    """
    course_code = models.CharField(max_length=20, unique=True, help_text="e.g., CS101, MATH201")
    course_name = models.CharField(max_length=200, help_text="Full course name")
    instructor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='courses_teaching',
        help_text="Instructor/Faculty for this course"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['course_code']
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class UserProfile(models.Model):
    """
    User profile extending Django's built-in User model.
    
    For Students:
        - Full name, email, student ID
        - Enrolled course
        - Fingerprint template
    
    For Instructors:
        - Can view attendance for their courses
        - Manage course data
    """
    
    # Role options for users
    ROLE_CHOICES = (
        ('instructor', 'Instructor'),  # Faculty/Teacher - can view attendance
        ('student', 'Student'),         # Student - can mark attendance
    )
    
    # Link to Django's built-in User model (one profile per user)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # User's role in the system
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # === STUDENT-SPECIFIC FIELDS ===
    # Full name of the student
    full_name = models.CharField(max_length=200, help_text="Student's full name")
    
    # Student ID number (unique identifier)
    student_id = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="Unique student ID number",
        null=True,
        blank=True
    )
    
    # Student email
    email = models.EmailField(unique=True, help_text="Student email address")
    
    # Course the student is enrolled in
    course = models.ForeignKey(
        Course, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students',
        help_text="Enrolled course"
    )
    
    # Store fingerprint template data (binary data from R307 sensor)
    fingerprint_template = models.BinaryField(blank=True, null=True)
    
    # Track if fingerprint is enrolled
    fingerprint_enrolled = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['full_name']
    
    def __str__(self):
        """String representation of user profile"""
        if self.role == 'student':
            return f"{self.full_name} ({self.student_id}) - {self.course.course_code if self.course else 'No Course'}"
        return f"{self.full_name} ({self.role})"

