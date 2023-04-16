from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')), 
]

urlpatterns += i18n_patterns(
    path('', include('base.urls')), #Auth & Tags
    path('', include('course.urls')), #courses
    path('', include('article.urls')), #Articles
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)