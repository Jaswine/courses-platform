from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField 
from django.contrib.auth.models import User
from course.models import Tag

#TODO: ARTICLE
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, default='')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    text = RichTextField(blank=True)
    public = models.BooleanField(default=False)
    
    likesForArticle = models.ManyToManyField(User, related_name='likesForArticle', blank=True, default=[])
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
        
    def __str__(self):
        return self.slug
    
#TODO: ARTICLE COMMENT
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.message
    