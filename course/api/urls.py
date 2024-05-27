from django.urls import path
from .views import courses, tags, titles, tasks

app_name = 'course'

urlpatterns = [
    # TODO: Tags
    path('tags', tags.tags_list_create, name='tags_list_create'),
    path('tags/<int:id>/', tags.tags_get_update_delete, name='tags_get_update_delete'),

    # TODO: Courses
    path('courses', courses.courses_list_create, name='courses_list_create'),
    path('courses/<int:id>/tasks', courses.course_show_tasks, name='course_show_tasks'),
    path('courses/<int:id>', courses.courses_get_update_delete, name='courses_get_update_delete'),
    path('courses-like/<int:id>', courses.course_add_like, name='course_add_like'),
    path('courses-like/<int:id>/add-to-course', courses.user_add_to_course, name='user_add_to_course'),
    path('courses/<int:id>/reviews', courses.course_reviews_show_create, name='course_reviews_show_create'),
    path('reviews/<int:id>', courses.course_reviews_delete, name='course_reviews_delete'),

    # TODO: TITLE
    path('courses/<int:id>/titles/', titles.title_list_create, name='title-list-create'),
    path('courses/titles/<int:id>/', titles.title_update_delete, name='title-update-delete'),
    path('courses/<int:id>/titles/<int:TitleID>/places/<int:NewOrder>/', titles.title_change_place, name='title-change-place'),

    path('courses/<int:id>/tasks/<int:task_id>/', tasks.task_get_update_delete, name='task-update-delete'),
]
