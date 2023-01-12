from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages 

def catalog(request):
    courses = Course.objects.all()
    
    context = {'cources': courses}
    return render(request, 'course/Catalog.html', context)

def course(request, slug):
    cource = Course.objects.get(slug=slug)
    titles = CourseTitle.objects.filter(course=cource.id)
    # tasks = 
    
    context = {'course': cource, 'titles': titles}
    return render(request, 'course/CourseInfo.html', context)

def createCourse(request):
    tags = Tag.objects.all()
    courses = Course.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = "-".join(title.lower().split(' '))
        user = request.user
        image = request.FILES['image']
        tag = request.POST.get('tag')
        about  = request.POST.get('about')
        whatAreUWillLearn = request.POST.get('WhatAreUWillLearn')
        level = request.POST.get('level')
        initialRequirements = request.POST.get('InitialRequirements')
        certificate = request.FILES['certificate']
        public = request.POST['public']
        
        if public == 'on': #! PUBLIC & UNPUBLIC
            public = True
        elif public == None:
            public = False
            
        if len(about) > 5: #! VALIDATION
            if (tag != None ): #! Tag Doesn't Selected
                if image != None: #! Image Doesn't Selected
                    if level != None: #!Level Doesn't Selected
                        if len(title) > 4:
                    
                            for course in courses:
                                if slug != course.slug: 
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
                                        certificate = certificate,
                                        public = public,
                                    )
                                    
                                    form.save()
                                    return redirect('cources:catalog')
                                else:
                                    messages.error(request, 'This article already exists')
                    
                        else:
                            messages.error(request, 'Title must be at least 4 characters')
                    else:
                        messages.error(request, 'Level must be selected')
                else:
                    messages.error(request, 'Image must be selected')
            else: 
                messages.error(request, 'Tag must be selected')
        else:
            messages.error(request, 'About must be at least 10 characters')
    
    context = {'tags': tags}
    return render(request, 'course/create/CreateCourse.html', context)