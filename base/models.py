from django.db import models
from django.contrib.auth.models import User
from course.models import Course, CourseTask

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='profiles', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    twitter = models.CharField(max_length=1000, blank=True)
    github = models.CharField(max_length=1000, blank=True)
    telegram = models.CharField(max_length=1000, blank=True)
    website = models.URLField(blank=True)
    
    #! Courses
    courses  = models.ManyToManyField(Course)
    tasks = models.ManyToManyField(CourseTask)
    
    #! Likes & Bookmarks
    likeCourses = models.ManyToManyField(Course, blank=True, related_name='likeCourses',  default='')
    bookmarkCourses = models.ManyToManyField(Course, blank=True, related_name='bookmarkCourses', default='')
    likeArticle = models.ManyToManyField(Course, blank=True, related_name='likeArticle',  default='')
    bookmarkArticle = models.ManyToManyField(Course, blank=True, related_name='likeBookmark',  default='')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
