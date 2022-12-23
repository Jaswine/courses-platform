from django.db import models
from django.contrib.auth.models import User
from base.models import Tag


#! ____________ARTICLE SECTION___________
#TODO: ARTICLE
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles', blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.title
    
#TODO: ARTICLE COMMENT
class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.message
    