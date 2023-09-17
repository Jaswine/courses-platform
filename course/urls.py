from django.urls import path
from .views import course, tags

app_name = 'course'

urlpatterns = [
    path('', course.courses, name='courses'),
    path('create', course.create_course, name='create_course'),
    path('<int:id>', course.course, name='course'),
    path('<int:id>/edit', course.course_edit, name='course-edit'),
    
    path('tags', tags.tags, name='tags'),
]
