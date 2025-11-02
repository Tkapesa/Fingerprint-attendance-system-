"""
============================================================
USER ADMIN CONFIGURATION
============================================================
Register UserProfile and Course models in Django admin panel.
============================================================
"""
from django.contrib import admin
from .models import UserProfile, Course


class CourseAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Course model.
    """
    list_display = ('course_code', 'course_name', 'instructor', 'created_at')
    list_filter = ('instructor', 'created_at')
    search_fields = ('course_code', 'course_name')
    ordering = ('course_code',)


class UserProfileAdmin(admin.ModelAdmin):
    """
    Custom admin interface for UserProfile model.
    """
    list_display = ('full_name', 'student_id', 'email', 'course', 'role', 'fingerprint_enrolled')
    list_filter = ('role', 'course', 'fingerprint_enrolled')
    search_fields = ('full_name', 'student_id', 'email', 'user__username')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')


# Register models with custom admin configurations
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


