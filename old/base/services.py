from django.contrib.auth.models import User
from course.models import  Tag, Course, CourseTask
from .models import Profile
from article.models import Article, ArticleComment

def get_filter_courses():
   return Course.objects.filter(public=True)[:8]

def get_filter_articles():
   return Article.objects.filter(public=True)[:8]

def user_filter_profile(name):
   return User.objects.filter(username=name)

def get_user(username):
   return  User.objects.get(username=username)

def get_user_profile(user):
   return Profile.objects.get(user=user)

def get_all_courses():
   return Course.objects.all()

def get_all_tags():
   return Tag.objects.all()