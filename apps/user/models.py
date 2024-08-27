from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    is_blocked = models.BooleanField(default=False)

    scores = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to='profiles', blank=True, default=None)
    backImage = models.ImageField(upload_to='back_images', blank=True, default=None)
    bio = RichTextField(max_length=1000, blank=True)
    location = models.CharField(max_length=168, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
