from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Authentication
    path('auth/', include('apps.authentication.urls')),
    
    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),
    
    # Attendance
    path('attendance/', include('apps.attendance.urls')),
    
    # Teacher app WITH namespace
    path('teacher/', include(('apps.teacher.urls', 'teacher'), namespace='teacher')),
    
    # Admin app WITH namespace
    path('admin-panel/', include(('apps.system_admin.urls', 'system_admin'), namespace='system_admin')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)