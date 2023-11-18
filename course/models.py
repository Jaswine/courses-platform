from django.db import models

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  #? RichTextUploadingField

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
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to=f'courses/{title}', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    #TODO: About this course
    # about = models.TextField(max_length=2000, blank=True)
    about = RichTextField(blank=True)
    level = models.CharField(max_length=13, choices=LEVEL)
      
    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)
    
    #TODO: Like & Participants
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    # participants = models.ManyToManyField(User, blank=True, related_name='participants')
    
    course_titles = models.ManyToManyField('Title', through='TitleOrder', blank=True, default=[],  related_name='course_titles')

    users_who_registered = models.ManyToManyField(User, related_name='users_who_registered', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.title

class Title(models.Model):
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    
    tasks = models.ManyToManyField('Task', through='TaskOrder', blank=True, default=[], related_name='tasks')
    
    def __str__(self):
        return self.title

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

    video = models.FileField(upload_to=f'courses/tasks/videos', blank=True)
    text = RichTextField(default="", blank=True)
    urls  = models.ManyToManyField("TaskURLField", default=[],  blank=True)
    questions = models.ManyToManyField("Question", default=[], blank=True)
    code_tasks = models.ManyToManyField("CodeTask", default=[], blank=True)

    # @classmethod    
    # def video_task(cls, video):
    #     return Task.objects.create(
    #         type = "video",
    #         video = video,
    #         text = ""
    #     )
        
    # @classmethod
    # def text_task(cls, text):
    #     return Task.objects.create(
    #         type = 'text',
    #         text = text,
    #     )
        
    # @classmethod    
    # def project_task(cls, text, urls):
    #     return Task.objects.create(
    #         type = "project",
    #         text = text,
    #         urls = urls
    #     )
                
    public = models.BooleanField(default=False)

    users_who_completed = models.ManyToManyField(User, related_name='users_who_completed_task', blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
  
# !:  _______________ Show Tasks __________________
# ?: Add Link on repo
class TaskURLField(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url_on_repo = models.URLField()
    
    def __str__(self) -> str:
        return self.url_on_repo

# ?: Question
class Question(models.Model):
    QUESTION_TYPES = (
        ("No answer choice", "No answer choice"),
        ("With a choice of one answer", "With a choice of one answer"),
    )

    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=QUESTION_TYPES)

    answers_to_choose = models.ManyToManyField("QuestionAnswersToChoose", blank=True)
    users_who_completed_question = models.ManyToManyField(User, related_name='users_who_completed_question', blank=True)

    correct_answer = models.CharField(max_length=200)

    @classmethod    
    def no_choice_question(cls):
        return Task.objects.create(
            type = "No answer choice",
        )
    
    @classmethod    
    def with_a_choice_question(cls, answers_to_choose):
        return Task.objects.create(
            type = "With a choice of one answer",
            answers_to_choose = answers_to_choose
        )
    
    def __str__(self) -> str:
        return self.title
    
class QuestionAnswersToChoose(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.title
    
# ?: Code Task
class CodeTask(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField()

    users_who_completed_code = models.ManyToManyField(User, related_name='users_who_completed_code', blank=True)

    def __str__(self) -> str:
        return self.title

# !: ____________ ORDERS _____________ 
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

