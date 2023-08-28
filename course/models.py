from django.db import models

from django.contrib.auth.models import User

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
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, default='')
    user = models.ManyToManyField(User)
    
    image = models.ImageField(upload_to='courses', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    #TODO: About this course
    about = models.TextField(max_length=2000, blank=True)
    whatAreUWillLearn = models.TextField(max_length=500, blank=True)
    knowledges = models.TextField(max_length=500, blank=True)
    level = models.CharField(max_length=13, choices=LEVEL)
    initialRequirements = models.TextField(max_length=500, blank=True)
      
    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)
    
    #TODO: Like & Bookmarks
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    
    course_titles = models.ManyToManyField('Title', through='TitleOrder', blank=True, default=[])
        
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.slug

class Title(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    
    course_tasks = models.ManyToManyField('Task', through='TaskOrder', blank=True, default=[])
    
    def __str__(self):
        return self.title

class Task(models.Model):
    TYPE = (
        ('text','text')
        ('video', 'video'),
    )
    
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE, blank=True)

    video = models.FileField(upload_to='courses/tasks/videos', blank=True)
    text = models.TextField(blank=True)
    
    @classmethod
    def video_task(cls, video):
        return Task.objects.create(
            type = "video",
            video = video,
        )
        
    @classmethod
    def text_task(cls, body):
        return Task.objects.create(
            type = 'text',
            body = body,
        )
        
    public = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
  
#!: ____________ ORDERS _____________ 
class TitleOrder(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  
        
class TaskOrder(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  
 
#!: ____________ PROGRESS _____________       
class UserTaskProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    points_earned = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)    
 
    def __str__(self):
        return self.user.username
 
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

