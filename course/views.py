from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 

def catalog(request):
    courses = Course.objects.filter(public=True)
    
    context = {'courses': courses}
    return render(request, 'course/Catalog.html', context)

def course(request, slug):
    course = Course.objects.get(slug=slug)
    titles = CourseTitle.objects.filter(course=course.id)
    # tasks = 
    
    context = {'course': course, 'titles': titles}
    return render(request, 'course/CourseInfo.html', context)

def createCourse(request):
    tags = Tag.objects.all()
    courses = Course.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = "-".join(title.lower().split(' '))
        user = request.user
        image = request.FILES.get('image', None)
        tag = request.POST.get('tag')
        about  = request.POST.get('about')
        whatAreUWillLearn = request.POST.get('WhatAreUWillLearn')
        level = request.POST.get('level')
        initialRequirements = request.POST.get('InitialRequirements')
                
        print(title)
            
        validated = True
            
        if len(about) < 4: #! VALIDATION
            validated = False
            messages.error(request, 'About must be at least 10 characters')
            
        if (tag == None ): #! Tag Doesn't Selected
            validated = False
            messages.error(request, 'Tag must be selected')
            
        if len(title) < 4: #! Title 
            validated = False
            messages.error(request, 'Title must be at least 4 characters')
                    
        for course in courses:
            if slug == course.slug: #! Slug
                validated = False
                messages.error(request, 'This article already exists')
                       
        if validated == True:
            tag = Tag.objects.get(id = tag)
                                            
            form = Course.objects.create( #! Create Course
                title = title,
                slug = slug,
                user = user,
                image = image,
                tags = tag,
                about = about,
                whatAreUWillLearn = whatAreUWillLearn,
                level = level,
                initialRequirements = initialRequirements,
                public = False,
            )
            print("Post Has Been Created")
        
            form.save()
            return redirect('profile/'+str(request.user.username)+'courses')
        else:
            messages.error(request, 'This article already exists')
            print("Post doesn't created")            
            
    context = {'tags': tags}
    return render(request, 'course/create/CreateCourse.html', context)