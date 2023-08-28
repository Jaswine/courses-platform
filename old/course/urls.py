from django.urls import path
from .views.course import show_all_courses_view, create_course_view, course, delete_course, task_view, delete_comment_view
from .views.course_panel import course_panel_tasks_view, course_panel_update_info, create_task_view, course_panel_update_title_view, update_task_view, delete_task_view, delete_title_view

app_name='course'

urlpatterns = [
   path('', show_all_courses_view, name='show_all_courses'),
   path('create', create_course_view, name='create_course'),
   
   path('courses/<str:slug>', course, name='course'),
   path('courses/<str:slug>/tasks/<int:pk>/', task_view, name='task_view'), 
   
   path('courses/<str:slug>/tasks/<int:pk>/comments/<int:comment_id>/', delete_comment_view, name='delete_comment'), 
   path('courses/<str:slug>/delete', delete_course, name='delete_course'),
   
   path('courses/<str:slug>/panel/tasks', course_panel_tasks_view, name='tasks-panel'),
   path('courses/<str:slug>/panel/update', course_panel_update_info, name='update-info-panel'),
   
   path('courses/<str:slug>/panel/titles/<int:title_id>/edit', course_panel_update_title_view, name='update-title'),
   path('courses/<str:slug>/panel/tasks/<int:task_id>/edit', update_task_view, name='update-task'),
   
    path('courses/<str:slug>/create-task', create_task_view, name='create-task'),
    
    path('courses/<str:slug>/panel/tasks/<int:task_id>/delete', delete_task_view, name='course-task-delete'),
    path('courses/<str:slug>/panel/titles/<int:title_id>/delete', delete_title_view, name='course-title-delete'),
]
