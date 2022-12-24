from django.urls import path
from .  import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #! REGISTRATION & LOGIN & LOGOUT
    path('registration', views.registration, name='registration'),
    path('login', views.home, name='login'),
]
