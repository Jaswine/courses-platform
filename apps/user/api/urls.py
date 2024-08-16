from django.urls import path
from apps.user.api.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard.registered_courses, name='dashboard'),
]