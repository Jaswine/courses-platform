from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('user.urls')),
    path('courses/', include('course.urls')),
    
    path('accounts/', include('allauth.urls')),
    
    path('api/', include('course.api.urls')),
]
