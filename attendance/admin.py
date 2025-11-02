"""
============================================================
ATTENDANCE ADMIN CONFIGURATION
============================================================
Register AttendanceLog model in Django admin panel.
Allows admins to view, search, and manage all attendance records.
============================================================
"""
from django.contrib import admin
from .models import AttendanceLog

class AttendanceLogAdmin(admin.ModelAdmin):
    """
    Custom admin interface for AttendanceLog.
    
    Features:
        - Display key fields in list view
        - Filter by status, course, and date
        - Search by student name, ID, username
        - Read-only timestamp (auto-generated)
    """
    # Columns to display in admin list view
    list_display = ('student_name', 'student_id', 'course', 'date', 'time', 'status', 'scan_method')
    
    # Add filters in sidebar
    list_filter = ('status', 'course', 'date', 'scan_method')
    
    # Enable search by student details
    search_fields = ('student_name', 'student_id', 'user__username')
    
    # Make timestamp fields read-only (they're auto-generated)
    readonly_fields = ('timestamp', 'date', 'time')
    
    # Order by most recent first
    ordering = ('-timestamp',)
    
    # Group fields in the detail view
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'student_name', 'student_id')
        }),
        ('Course Information', {
            'fields': ('course',)
        }),
        ('Attendance Details', {
            'fields': ('status', 'scan_method', 'timestamp', 'date', 'time')
        }),
    )

# Register with custom admin configuration
admin.site.register(AttendanceLog, AttendanceLogAdmin)


