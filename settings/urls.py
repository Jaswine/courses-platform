from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('base.urls')), #Auth & Tags
    path('', include('course.urls')), #Cources
    path('', include('article.urls')), #Articles
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
