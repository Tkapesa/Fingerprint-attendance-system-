from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # This will be /auth/
    path('login/student/', views.login_student, name='login_student'),
    path('login/teacher/', views.login_teacher, name='login_teacher'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_view, name='logout'),
]