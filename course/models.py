from django.db import models

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  #? RichTextUploadingField
import datetime


#!: ______ TAG FOR COURSES & ARTICLES________
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
#!: ____________ COURSE _____________
class Course(models.Model):
    LEVEL = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    )
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='courses', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    #TODO: About this course
    # about = models.TextField(max_length=2000, blank=True)
    about = RichTextField(max_length=2000, blank=True)
    level = models.CharField(max_length=13, choices=LEVEL)
      
    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)
    
    #TODO: Like & Participants
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    # participants = models.ManyToManyField(User, blank=True, related_name='participants')
    
    # titles = models.ManyToManyField('Title', through='TitleOrder', blank=True, default=[],  related_name='titles')
    tasks = models.ManyToManyField('Task', through='TaskOrder', blank=True, default=[], related_name='tasks')

    users_who_completed_course = models.ManyToManyField(User, related_name='users_who_completed_course', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title

# class Title(models.Model):
#     title = models.CharField(max_length=255)
#     public = models.BooleanField(default=False)
    
#     tasks = models.ManyToManyField('Task', through='TaskOrder', blank=True, default=[], related_name='tasks')
    
#     def __str__(self):
#         return self.title

class TaskURLField(models.Model):
    url_on_repo = models.URLField()
    
    def __str__(self) -> str:
        return self.url_on_repo

class Task(models.Model):
    TYPE = (
        ('text','text'),
        ('video', 'video'),
        ('project','project'),
        ('code', 'code'),
    )
    
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE, blank=True)
    points = models.IntegerField(default=0)

    video = models.FileField(upload_to='courses/tasks/videos', blank=True)
    text = RichTextField(blank=True)
    url_on_repo  = models.ManyToManyField(TaskURLField, blank=True)
    code_true_answer = models.CharField(max_length=255, blank=True)
    
    @classmethod    
    def video_task(cls, video):
        return Task.objects.create(
            type = "video",
            video = video,
        )
        
    @classmethod
    def text_task(cls, text):
        return Task.objects.create(
            type = 'text',
            text = text,
        )
        
    @classmethod    
    def project_task(cls, text, url_on_repo):
        return Task.objects.create(
            type = "project",
            text = text,
            url_on_repo = url_on_repo
        )
        
    @classmethod    
    def project_task(cls, text, code_true_answer):
        return Task.objects.create(
            type = "code",
            text = text,
            url_on_repo = code_true_answer
        )
                
    public = models.BooleanField(default=False)
    
    users_who_completed = models.ManyToManyField(User, related_name='users_who_completed_task', blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
  
#!: ____________ ORDERS _____________ 
# class TitleOrder(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     title = models.ForeignKey(Title, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField()

#     class Meta:
#         ordering = ['order']  
        
class TaskOrder(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  
 
# #!: ____________ PROGRESS _____________       
# class UserCourseProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
#     points_earned = models.PositiveIntegerField(default=0)
#     completed = models.BooleanField(default=False) 
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
       
#     def __str__(self):
#         return self.user.username
 
#!: ____________ COMMENTS _____________       
class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    message = models.TextField(blank=True, max_length=1000)
    stars = models.IntegerField(default=0, blank=True)
        
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        self.course.title

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    text = models.TextField(blank=True, max_length=1000)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.courseTask.title

