"""
   ! DB STRUCTURE:  https://www.figma.com/community/file/1188090535052678707
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True)
    # image = models.ImageField(upload_to='', blank=True, null=True)
    bio = models.TextField(max_length=500)
    
    def __str__(self):
        return self.email

#!: ______TAG FOR COURSES & ARTICLES
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

