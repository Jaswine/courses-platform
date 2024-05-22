from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('user.urls')),
    path('courses/', include('course.urls')),
    
    path('accounts/', include('allauth.urls')),
    
    path('api/', include('course.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
