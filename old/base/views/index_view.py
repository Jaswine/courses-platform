from django.shortcuts import render, redirect
from course.models import Course
from article.models import Article

def index(request):
   # # get data
   courses = Course.objects.filter(public=True)
   articles = Article.objects.filter(public=True)
      
   context = {
      'courses': courses, 
      'articles': articles
   }
   return render(request, 'base/index.html', context)

