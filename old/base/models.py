from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from course.models import Course, CourseTask
from article.models import Article

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scores = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='profiles', blank=True, default=None)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=168, blank=True)

    instagram = models.CharField(max_length=1000, blank=True)
    facebook = models.CharField(max_length=1000, blank=True)
    number = models.CharField(max_length=12, blank=True)
    twitter = models.CharField(max_length=1000, blank=True)
    github = models.CharField(max_length=1000, blank=True)
    telegram = models.CharField(max_length=1000, blank=True)
    website = models.URLField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
   

       
   