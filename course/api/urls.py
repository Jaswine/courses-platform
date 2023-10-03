from django.urls import path
from .views import courses, tags, tasks

app_name = 'course'

urlpatterns = [
    # Courses
    path('courses', courses.courses_list_create, name='courses_list_create'),
    path('courses/<int:id>', courses.courses_get_update_delete, name='courses_get_update_delete'),
    path('courses-like/<int:id>', courses.course_add_like, name='course_add_like'),
    
    # Tasks
    path('courses/<int:id>/tasks', tasks.tasks_list, name='tasks_list_create'),
    path('courses/<int:id>/tasks/<int:task_id>/change-place/to/<int:new_order>', tasks.change_task_place, name='change_task_place'),
    
    # Tags
    path('tags', tags.tags_list_create, name='tags_list_create'),
    path('tags/<int:id>/', tags.tags_get_update_delete, name='tags_get_update_delete'),
]
