from django.urls import path
from .views import courses, tags, titles, tasks, task_comment

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

    # TODO: TASK
    path('courses/<int:id>/tasks/<int:task_id>/', tasks.task_get_update_delete, name='task-update-delete'),
    path('courses/<int:id>/tasks/<int:task_id>/experiense/', tasks.task_add_experiense, name='task_add_experiense'),
    path('courses/<int:course_id>/tasks/<int:task_id>/bookmarks/', tasks.task_add_remove_bookmark, name='task_add_remove_bookmark'),

    # TODO: TASK COMMENTS
    path('courses/tasks/<int:task_id>/comments', task_comment.task_comment_list_create, name='task_comment_list_create'),
    path('courses/tasks/<int:task_id>/comments/<int:comment_id>/delete', task_comment.task_comment_update_delete, name='task_comment_update_delete'),
    # path('courses/tasks/<int:task_id>/comments/<int:comment_id>/react', task_comment.task_comment_react, name='task_comment_react'),
]
