from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create-session/', views.create_session, name='create_session'),
    path('session/<str:session_id>/', views.view_session, name='view_session'),
    path('session/<str:session_id>/end/', views.end_session, name='end_session'),
    path('reports/', views.attendance_reports, name='attendance_reports'),
    path('manage-students/', views.manage_students, name='manage_students'),
]
