from django.urls import path
from user.api.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard.registered_courses, name='dashboard'),
]