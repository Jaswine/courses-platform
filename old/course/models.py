from django.db import models
from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User


# Create your models here.
#!: ______TAG FOR COURSES & ARTICLES
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    #!: ____________COURSE_____________
class Course(models.Model):
    LEVEL = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    )
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='courses', blank=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    #TODO: About this course
    about = models.TextField(max_length=2000, blank=True)
    whatAreUWillLearn = models.TextField(max_length=500, blank=True)
    level = models.CharField(max_length=13, choices=LEVEL)
    initialRequirements = models.TextField(max_length=500, blank=True)
    certificate = models.ImageField(upload_to='courses/certificates', blank=True)
      
    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)
    
    #TODO: Like & Bookmarks
    likes = models.ManyToManyField(User, blank=True, related_name='likes' )
    
    course_titles = models.ManyToManyField('CourseTitle', blank=True, default=[])
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title
    
#!  ____________TITLE FOR CHAPTER COURSE_____________
class CourseTitle(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    tasks = models.ManyToManyField('CourseTask', blank=True, default=[])
    
    public  = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

#! Course Task
class CourseTask(models.Model):
    TASKSTYPE = (
        ('video', 'video'),
        ('code', 'code'),
        ('test', 'test'),
        ('text','text')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    
    taskType = models.CharField(max_length=10, choices=TASKSTYPE, blank=True)
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
        
    video = models.FileField(upload_to='courses/tasks/videos', blank=True)
    body = RichTextField(blank=True)
    codeAnswer = models.TextField(blank=True)
    
    public = models.BooleanField(default=False)
    
    @classmethod
    def video_task(cls, video):
        return CourseTask.objects.create(
            taskType = "video",
            video = video,
        )
    
    @classmethod
    def code_task(cls, text, codeAnswer):
        return CourseTask.objects.create(
            taskType = 'code', 
            body = body,
            codeAnswer = codeAnswer,
        )
        
    @classmethod
    def text_task(cls, body):
        return CourseTask.objects.create(
            taskType = 'text',
            body = body,
        )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
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
    courseTask = models.ForeignKey(CourseTask, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True, max_length=1000)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.courseTask.title
    