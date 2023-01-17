from django.urls import path 
from . import views

app_name='courses'

urlpatterns = [
    path('courses', views.catalog, name='catalog'),
    path('courses/<str:slug>', views.course, name='course'),
    
    path('create-course', views.createCourse, name='create-course'),
    
    #Panel
    path('courses/<str:slug>/tasks-panel', views.TasksPanel, name='tasks-panel'),
    path('courses/<str:slug>/update-info-panel', views.updateInfoPanel, name='update-info-panel'),
    path('courses/<str:slug>/update-info-panel/create-task', views.createTask, name='create-task'),
]
