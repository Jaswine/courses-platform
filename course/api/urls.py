from django.urls import path
from .views import courses, tags, tasks

app_name = 'course'

urlpatterns = [
    # Courses
    path('courses', courses.courses_list_create, name='courses_list_create'),
    path('courses/<int:id>/tasks', courses.course_show_tasks, name='course_show_tasks'),
    path('courses/<int:id>', courses.courses_get_update_delete, name='courses_get_update_delete'),
    path('courses-like/<int:id>', courses.course_add_like, name='course_add_like'),
    path('courses-like/<int:id>/add-to-course', courses.user_add_to_course, name='user_add_to_course'),
    path('courses/<int:id>/reviews', courses.course_reviews_show_create, name='course_reviews_show_create'),
    path('reviews/<int:id>', courses.course_reviews_delete, name='course_reviews_delete'),

    # Tasks
    path('courses/edit/<int:id>/tasks', tasks.tasks_list, name='tasks_list_create'),
    path('courses/edit/<int:id>/tasks/<int:task_id>/change-place/to/<int:new_order>', tasks.change_task_place, name='change_task_place'),
    path('tasks/<int:id>/add-to-task', tasks.task_add_user, name='task_add_user'),
    
    # Tags
    path('tags', tags.tags_list_create, name='tags_list_create'),
    path('tags/<int:id>/', tags.tags_get_update_delete, name='tags_get_update_delete'),
]
