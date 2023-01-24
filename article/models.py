from django.db import models
from django.contrib.auth.models import User
from course.models import Tag
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


#! ____________ARTICLE SECTION___________
#TODO: ARTICLE
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, default='')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    text = RichTextField(blank=True)
    public = models.BooleanField(default=False)
    
    #TODO: LIKES
    likesForArticle = models.ManyToManyField(User, related_name='likesForArticle', blank=True)
    bookmarksForCourse = models.ManyToManyField(User, related_name='bookmarksForCourse', blank=True)
    
    #TODO: STATISTIC
    commentsCount = models.IntegerField(default=0)
    
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
    # answer_on = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    message = models.TextField(max_length=500)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.message
    