import uuid

from django.db import models

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  #? RichTextUploadingField

from user.models import Reaction


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

    image = models.ImageField(upload_to='courses', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    #TODO: About this course
    about = RichTextField(blank=True)
    level = models.CharField(max_length=13, choices=LEVEL)

    #TODO: Public or Unpublic
    public = models.BooleanField(default=False)

    #TODO: Like & Participants
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    course_titles = models.ManyToManyField('Title', through='TitleOrder', blank=True, default=[],
                                           related_name='course_titles')

    users_who_registered = models.ManyToManyField(User, related_name='users_who_registered', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

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
        ('TaskText', 'TaskText'),
        ('TaskVideo', 'TaskVideo'),
        ('TaskProject', 'TaskProject'),
        ('TaskQuestions', 'TaskQuestions'),
        ('TaskCode', 'TaskCode'),
    )

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE, blank=True)
    points = models.IntegerField(default=0)
    bookmarks = models.ManyToManyField(User, related_name='task_bookmarks', blank=True)

    def task_directory_path(instance, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{instance.id}_document_{uuid.uuid4().hex[:10]}.{extension}'
        return f'courses/tasks/{instance.id}/video/{new_filename}'

    video = models.FileField(upload_to=task_directory_path, blank=True)
    text = RichTextField(default="", blank=True)
    urls = models.ManyToManyField("TaskURLField", default=[], blank=True)
    questions = models.ManyToManyField("Question", default=[], blank=True)
    code_tasks = models.ManyToManyField("CodeTask", default=[], blank=True)

    @classmethod
    def video_task(cls, text, video):
        return Task.objects.create(
            type="TaskVideo",
            video=video,
            text=text,
        )

    @classmethod
    def text_task(cls, text):
        return Task.objects.create(
            type='TaskText',
            text=text,
        )

    @classmethod
    def project_task(cls, text, urls):
        return Task.objects.create(
            type="TaskProject",
            text=text,
            urls=urls
        )

    @classmethod
    def questions_task(cls, text, questions):
        return Task.objects.create(
            type="TaskQuestions",
            text=text,
            questions=questions
        )

    @classmethod
    def code_task(cls, text, code_tasks):
        return Task.objects.create(
            type="TaskCode",
            text=text,
            code_tasks=code_tasks
        )

    public = models.BooleanField(default=False)

    users_who_completed = models.ManyToManyField(User, related_name='users_who_completed_task', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.title + ' - ' +
                self.type + ' - ' +
                str(self.points))


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

    correct_answer = models.CharField(max_length=200)

    @classmethod
    def no_choice_question(cls):
        return Task.objects.create(
            type="No answer choice",
        )

    @classmethod
    def with_a_choice_question(cls, answers_to_choose):
        return Task.objects.create(
            type="With a choice of one answer",
            answers_to_choose=answers_to_choose
        )

    def __str__(self) -> str:
        return self.title


class QuestionAnswersToChoose(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.title


# ?: Code Task
class CodeTask(models.Model):
    title = models.TextField()
    code = models.TextField()

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
    task_comment_parent = models.ForeignKey('self',
                                            on_delete=models.CASCADE,
                                            blank=True,
                                            null=True,
                                            related_name='task_comment_children')

    text = models.TextField(max_length=1000)

    likes = models.ManyToManyField(User, related_name='taskCommentLikes', blank=True)
    complaints = models.ManyToManyField(User, through='TaskCommentUserComplaint',
                                        related_name='task_comment_complaints',
                                        default=[], blank=True)
    
    is_public = models.BooleanField(default=True,
                                    blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return ('Задание: "' + self.task.title + '" - ' +
                "Создатель: " + self.user.username + ' - ' +
                "Сообщение: " + self.text)


class TaskCommentUserComplaint(models.Model):
    COMPLAINT_TYPES = (
        ('Unwanted advertising or spam', 'Unwanted advertising or spam'),
        ('Pornography or explicit sex scenes', 'Pornography or explicit sex scenes'),
        ('Discriminatory language or naturalistic content', 'Discriminatory language or naturalistic content'),
        ('Propaganda of terrorism', 'Propaganda of terrorism'),
        ('Harassment or bullying', 'Harassment or bullying'),
        ('Suicide or self-mutilation', 'Suicide or self-mutilation'),
        ('False information', 'False information'),
    )

    taskComment = models.ForeignKey(TaskComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=100, choices=COMPLAINT_TYPES)
    message = models.TextField(max_length=1500, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return ('ID комментария: "' + str(self.taskComment.id) + '" - ' +
                'Пользователь: "' + self.user.username + '" - ' +
                'Тип: "' + self.type + '"')
