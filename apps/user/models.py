import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.template.defaultfilters import default


class User(AbstractUser):
    """
        Пользователь
    """
    is_blocked = models.BooleanField(default=False)
    scores = models.IntegerField(default=0)

    def user_image_path(self, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{self.username}_document_{uuid.uuid4().hex[:10]}.{extension}'
        return f'profiles/{self.username}/images/{new_filename}'

    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)

    def user_back_image_path(self, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{self.username}_document_{uuid.uuid4().hex[:10]}.{extension}'
        return f'users/{self.username}/back-images/{new_filename}'
    
    backImage = models.ImageField(upload_to=user_back_image_path, blank=True, null=True)

    bio = RichTextField(max_length=1000, blank=True, default='')
    location = models.CharField(max_length=168, blank=True, default='')

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username


class Reaction(models.Model):
    """
        Реакция
    """
    REACTION_CHOICES = [
        ('Like', 'Like'),
        ('Dislike', 'Dislike'),
        ('Heart', 'Heart'),
        ('Unicorn', 'Unicorn'),
        ('Clap', 'Clap'),
        ('Fire', 'Fire'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reacted with {self.get_reaction_type_display()}"


class Achievement(models.Model):
    """
        Достижение
    """
    ACHIEVEMENT_TYPES = (
        ('courses', 'Courses Completed'),
        ('tasks', 'Tasks Completed'),
        ('comments', 'Comments Made'),
        ('days', 'Days Active'),
    )

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000, default='', blank=True)
    type = models.CharField(max_length=10, choices=ACHIEVEMENT_TYPES)
    target_value = models.PositiveIntegerField()

    def achievement_image_path(self, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{self.id}_document_{uuid.uuid4().hex[:10]}.{extension}'
        return f'achievements/{self.id}/images/{new_filename}'

    image = models.ImageField(upload_to=achievement_image_path, blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', '-updated')

    def __str__(self):
        return f'{self.title} ({self.get_type_display()}: {self.target_value})'


class UserAchievement(models.Model):
    """
        Прогресс пользователя за достижение
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE,
                                    related_name='user_achievements')
    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    date_earned = models.DateTimeField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title} (Progress: {self.progress}/{self.achievement.target_value})"