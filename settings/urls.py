from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('auth.urls')),
    path('course/', include('course.urls')),
]
