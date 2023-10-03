from django.urls import path
from .views import course, tags

app_name = 'course'

urlpatterns = [
    path('', course.courses, name='courses'),
    path('create', course.create_course, name='create_course'),
    path('<int:id>', course.course, name='course'),
    path('<int:id>/edit', course.course_edit, name='course-edit'),
    path('<int:id>/delete', course.course_delete, name='course-delete'),
    
    # Tasks
    path('<int:id>/edit/tasks', course.course_edit_tasks, name='course-edit-tasks'),
    path('<int:id>/edit/tasks/<int:task_id>/edit', course.course_task_update, name='course_tasks_update'),
    path('<int:id>/edit/tasks/<int:task_id>/delete', course.course_task_delete, name='course_task_delete'),
    path('<int:id>/tasks-create', course.course_task_create, name='course_tasks_create'),
    
    path('tags', tags.tags, name='tags'),
]
