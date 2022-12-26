from django.urls import path 
from . import views

app_name='cources'

urlpatterns = [
    path('cources', views.catalog, name='catalog'),
    path('cources/<str:slug>', views.course, name='course'),
]
