from .models import Article, ArticleComment
from course.models import Tag

def get_all_articles():
   return Article.objects.all()

def get_one_article(slug):
   return Article.objects.get(slug = slug)

def get_all_tags():
   return Tag.objects.all()

def article_comments_filter(article):
   return ArticleComment.objects.filter(article=article)

def articles_list_filter_tags(tag):
   return Article.objects.filter(tag = tag)

def article_get_one_comment(id):
   return ArticleComment.objects.get(id=id)