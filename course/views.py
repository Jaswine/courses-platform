from django.shortcuts import render
from .models import *

def catalog(request):
    cources = Course.objects.all()
    
    context = {'cources': cources}
    return render(request, 'course/Catalog.html', context)

def course(request, slug):
    cource = Course.objects.get(slug=slug)
    titles = CourseTitle.objects.filter(course=cource.id)
    # tasks = 
    
    context = {'course': cource, 'titles': titles}
    return render(request, 'course/CourseInfo.html', context)

def createCourse(request):
    tags = Tag.objects.all()
    
    context = {'tags': tags}
    return render(request, 'course/create/CreateCourse.html', context)