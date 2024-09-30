from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('apps.user.urls')),
    path('courses/', include('apps.course.urls')),
    path('articles/', include('apps.article.urls')),

    path('accounts/', include('allauth.urls')),
    
    path('api/courses/', include('apps.course.api.urls')),
    path('api/article/', include('apps.article.api.urls')),
    path('api/user/', include('apps.user.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
