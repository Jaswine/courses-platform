from django.urls import path
from .views import course, tags

app_name = 'course'

urlpatterns = [
    path('', course.courses, name='courses'),
    path('create', course.create_course, name='create_course'),
    
    path('tags', tags.tags, name='tags'),
]
