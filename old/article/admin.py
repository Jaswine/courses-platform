from django.contrib import admin
from .models import Article, ArticleComment

admin.site.register(Article)
admin.site.register(ArticleComment)