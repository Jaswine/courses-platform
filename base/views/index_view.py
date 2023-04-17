from django.shortcuts import render, redirect

def index(request):
   # # get data
   # courses = get_filter_courses(True)
   # articles = get_filter_articles(True)
   
   # context = {
   #    'courses': courses, 
   #    'articles': articles
   # }
   return render(request, 'base/index.html')

