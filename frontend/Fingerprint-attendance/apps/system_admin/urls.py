from django.urls import path
from . import views

app_name = 'system_admin'

urlpatterns = [
    # path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-role/<str:user_id>/', views.update_user_role, name='update_user_role'),
    path('enroll/', views.enroll_fingerprint, name='enroll_fingerprint'),
]
