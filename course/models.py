from django.db import models
from django.contrib.auth.models import User


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
    image = models.ImageField(upload_to='courses', blank=True, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    #TODO: About this course
    about = models.TextField(max_length=2000, blank=True)
    whatAreUWillLearn = models.TextField(max_length=500, blank=True)
    level = models.CharField(max_length=13, choices=LEVEL, null=True)
    initialRequirements = models.TextField(max_length=500, blank=True)
    # certificate = models.FileField(upload_to='courses/certificates', blank=True, null=True)
    
    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)
    
    #TODO: Statistics
    lessonsCount = models.IntegerField(default=0)
    themesCount = models.IntegerField(default=0)
    commentsCount = models.IntegerField(default=0)
    viewCount = models.IntegerField(default=0)
    
    #TODO: Like & Bookmarks
    likes = models.ManyToManyField(User, blank=True, related_name='likes' )
    bookmarks = models.ManyToManyField(User, blank=True, related_name='bookmarks')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.title

#!  ____________TITLE FOR CHAPTER COURSE_____________
class CourseTitle(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    public = models.BooleanField(default=False)
    
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
    
    courseTitle = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
    task = models.CharField(max_length=10, choices=TASKSTYPE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
        
    video = models.FileField(upload_to='videos', blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    codeAnswer = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    
    public = models.BooleanField(default=False)
    
    @classmethod
    def video_task(cls, title, description, video, public):
        return CourseTask.objects.create(
            task = "video",
            title = title,
            description = description,
            video = video,
            public = public,
        )
    
    @classmethod
    def code_task(cls, title, description, codeAnswer, public):
        return CourseTask.objects.create(
            task = 'code', 
            title = title,
            description = description,
            codeAnswer = codeAnswer,
            public = public,
        )
        
    @classmethod
    def article_task(cls, title, description, public):
        return CourseTask.objects.create(
            task = 'text',
            title = title,
            description = description,
            public = public,    
        )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.title
    
class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.message