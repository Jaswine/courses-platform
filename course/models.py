from django.db import models
from django.contrib.auth.models import User


#!: ______TAG FOR COURSES & ARTICLES
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


#!: ____________COURSE_____________
class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', blank=True, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, blank=True)
    
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

#!  ____________TITLE FOR CHAPTER COURSE_____________
class CourseTitle(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

#!  _______________TASKS_____________
#TODO: COURSE VIDEO
# class CourseVideo(models.Model):
#     courseTitle = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     video = models.FileField(upload_to='videos', blank=True, null=True)
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.title
    
# # ?  COURSE VIDEO COMMENTS
# class CourseVideoComment(models.Model):
#     courseVideo = models.ForeignKey(CourseVideo, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField(max_length=500)
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-updated', '-created']
        
#     def __str__(self):
#         return self.message

# #TODO: WRITE CODE
# class WriteCode(models.Model):
#     courseTitle = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     truethCode = models.TextField()
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.title

# #? WRITE CODE COMMENT
# class WriteCodeComment(models.Model):
#     writeCode = models.ForeignKey(WriteCode, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField(max_length=500)
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-updated', '-created']
        
#     def __str__(self):
#         return self.message
    

#TODO: CODE QUESTIONS
# class Question(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     answer = models.CharField()
    
#     def __str__(self):
#         return self.title
    
# class CodeTest(models.Model):
#     courseTitle = models.ForeignKey(CourseTitle, on_delete=models.CASCADE)
#     questions  = models.ManyToManyField(Question)
#     title = models.CharField(max_length=255)
#     description = models.TextField(max_length=500, blank=True)
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-updated', '-created']

# #? WRITE CODE COMMENT
# class CodeTestComment(models.Model):
#     codeTest = models.ForeignKey(CodeTest, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField(max_length=500)
    
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ['-updated', '-created']
        
#     def __str__(self):
#         return self.message

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
    
    @classmethod
    def video_task(cls, title, description, video):
        return CourseTask.objects.create(
            task = "video",
            title = title,
            description = description,
            video = video,
        )
    
    @classmethod
    def code_task(cls, title, description, codeAnswer):
        return CourseTask.objects.create(
            task = 'code', 
            title = title,
            description = description,
            codeAnswer = codeAnswer,
        )
        
    @classmethod
    def article_task(cls, title, description):
        return CourseTask.objects.create(
            task = 'text',
            title = title,
            description = description            
        )
        
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.title
    
