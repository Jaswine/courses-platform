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
    reviews = CourseComment.objects.filter(course=course,commentType = 'review')
    
    courseTitlesCount = titles.count()
    courseTasksCount = CourseTask.objects.filter(course = course).count()
    courseCommentsCount = reviews.count
    likes = course.likes.count
    
    commentPermission = True
    for i in reviews:
        if i.user.username == request.user.username:
            commentPermission = False   
    
    if request.user.is_authenticated:
        if request.method == 'POST': #! FOR LIKES
            type = request.POST.get('type')
            if type == 'like':
                status = False
                
                for like in course.likes.all():
                    if like.username == request.user.username:
                        status = True      
                
                if status:
                    course.likes.remove(like)
                else:
                    course.likes.add(request.user)
                    course.save()
            elif type == 'review': #! FOR REVIEWS
                message = request.POST.get('message')
                stars = request.POST.get('stars')
                user = request.user
                
                print(message)
                form = CourseComment.objects.create(
                    course = course,
                    commentType = 'review',
                    user = user,
                    rating = stars,
                    message = message,
                )
                form.save()
                return redirect('/courses/'+ str(course.slug)+'#reviews')
            else:
                messages.error(request, 'u need to choose some stars If u wanna send message')
    else:
        messages.error(request, 'u need to sign in or sign up')
                
    context = {
        'course': course, 
        'titles': titles,
        
        'courseTitlesCount': courseTitlesCount,
        'courseTasksCount': courseTasksCount,
        'courseCommentsCount': courseCommentsCount,
        
        'likes': likes,
        'reviews': reviews,
        
        'commentPermission': commentPermission,
    }
    return render(request, 'course/CourseInfo.html', context)

def deleteReview(request,slug, id):
    if request.user.is_authenticated:
        comment =  CourseComment.objects.get(id=id)
        if request.user.username == comment.user.username:
            comment.delete()
            return redirect('/courses/'+ str(slug)+'#reviews')

def task(request, slug, pk):
    course = Course.objects.get(slug=slug)
    tasksAll = CourseTask.objects.filter(course=course).reverse()
    task = CourseTask.objects.get(id=pk)
    titles = CourseTitle.objects.filter(course=course.id)
    comments = CourseComment.objects.filter(course=course, courseTask=task)
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        
        form = CourseComment.objects.create(
            commentType = 'comment',
            course = course,
            user = request.user,
            message = comment,
            courseTask = task,
        )
        
        form.save()
        return redirect('courses:task', course.slug, task.id)
    
    context = {
        'course': course,
        'titles': titles,
        'tasks': tasksAll,
        'task': task,
        'comments': comments
    }
    return render(request, 'course/Task.html', context)

def courseTaskCommentDelete(request, slug, pk, comment_id):
    course = Course.objects.get(slug=slug)
    task = CourseTask.objects.get(id=pk)
    courseComment = CourseComment.objects.get(id=comment_id)
    
    if courseComment:
        if request.user.username == courseComment.user.username:
            courseComment.delete()
            return redirect('courses:task', course.slug, task.id)    
        else: 
            messages.error(request, 'I think, u are not the author this comment')
    else:
        messages.error(request, 'comment not found')

def createCourse(request):
    tags = Tag.objects.all()
    courses = Course.objects.all()
    
    if request.method == 'POST':
        title = request.POST['title']
        slug = "-".join(title.lower().split(' '))
        user = request.user
        image = request.FILES.get('image', None)
        tag = request.POST.get('tag')
        about  = request.POST.get('about')
        whatAreUWillLearn = request.POST.get('WhatAreUWillLearn')
        level = request.POST.get('level')
        initialRequirements = request.POST.get('InitialRequirements')
        
        validated = True
            
        if len(about) < 4: #! VALIDATION
            validated = False
            messages.error(request, 'About must be at least 10 characters')
            
        if (tag == None ): #! Tag Doesn't Selected
            validated = False
            messages.error(request, 'Tag must be selected')
            
        if len(title) < 10: #! Title 
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
            return redirect('profile/'+str(request.user.username)+'/courses')
        else:
            messages.error(request, 'This article already exists')
            print("Post doesn't create")            
            
    context = {'tags': tags}
    return render(request, 'course/create/CreateCourse.html', context)

def updateInfoPanel(request, slug):
    page = 'UpdateInfoPanel'
    course = Course.objects.get(slug=slug)
    courses = Course.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        
        courseImage = course.image 
        #if u don't choice image, we get last image or None
        
        if courseImage == '' or courseImage == ' ':
            courseImage = None
            
        image = request.FILES.get('image', courseImage)
        tagId = request.POST.get('tag')
        about = request.POST.get('about')
        WhatAreUWillLearn = request.POST.get('WhatAreUWillLearn')
        level = request.POST.get('level')
        initialRequirements = request.POST['InitialRequirements']
        public = request.POST.get('public')
        
        if public == 'on':
            public = True
        else: 
            public = False
            
        tag = Tag.objects.get(id = tagId) # GET TAG FOR UPDATE
        
        validated = True
            
        if len(about) < 10: #! VALIDATION
            validated = False
            messages.error(request, 'About must be at least 10 characters')
            
        if (tag == None ): #! Tag Doesn't Selected
            validated = False
            messages.error(request, 'Tag must be selected')
            
        if len(title) < 4: #! Title 
            validated = False
            messages.error(request, 'Title must be at least 4 characters')
            
        if len(title) > 100: # ! TITLE
            validated = False
            messages.error(request, 'Title must be at more than 100 symbols characters')
            
        if len(title) > 100: # ! TITLE
            validated = False
            messages.error(request, 'Title must be at more than 100 symbols characters')
            
        if len(WhatAreUWillLearn) < 10:  #! What Are U Will Learn
            validated = False
            messages.error(request, 'WhatAreUWillLearn must be at least 10 characters')
        
        if len(WhatAreUWillLearn) > 500: #! What Are U Will Learn
            validated = False
            messages.error(request, 'What Are U Will Learn must be at more than 500 symbols characters')
            
        print('________________',level)             
        if validated == True:
            if course.title != title:
                course.title = title
            if course.image != image:
                course.image = image
            if course.about != about:
                course.about = about
            if course.tags.id != tag.id:
                course.tags = tag
            if course.whatAreUWillLearn != WhatAreUWillLearn:
                course.whatAreUWillLearn = WhatAreUWillLearn
            if course.level != level and level != None and level != 'None':
                course.level = level
            if course.initialRequirements != initialRequirements:
                course.initialRequirements = initialRequirements
            if course.public != public:
                course.public = public
            
            course.save()
            return redirect('courses:course', course.slug)
    
    context = {
        'page': page, 
        'course': course, 
        'tags': tags
    }
    return render(request, 'course/panel/coursePanel.html',context)  

def TasksPanel(request, slug):
    page = 'TasksPanel'
    course = Course.objects.get(slug=slug)
    CourseTitles = CourseTitle.objects.filter(course=course)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        
        if len(title) > 3:
            form = CourseTitle.objects.create(
                title=title,
                course=course,
                public = True,
                place = CourseTitles.count() + 1,
                # tasks = []
                user = request.user
            )
            form.save()
            
            return redirect('/courses/'+str(course.slug)+'/tasks-panel')
    
    context = {'page': page, 'course': course, 'CourseTitles': CourseTitles} 
    return render(request, 'course/panel/coursePanel.html', context)

def createTask(request, slug):
    page = 'create_task'
    course = Course.objects.get(slug=slug)
    CourseTitles = CourseTitle.objects.filter(course =course)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_title = request.POST.get('course_title')
        tag = request.POST.get('tag')
        public = True
        
        validated = True
        
        if len(title) < 4:
            validated = False
            messages.error(request, 'Title must be at least 4 characters')
            
        if course_title == None or course_title == '':
            validated = False
            messages.error(request, 'Course Title is None')
            
        if course == None or course == '':
            validated = False
            messages.error(request, 'Course is None')

        if tag == None or tag == '':
            validated = False
            messages.error(request, 'Tag is None')
        
        if tag == 'text':
            body = request.POST.get('body')
            oneCourseTitle = CourseTitle.objects.get(id=course_title)
            
            if validated:
                if request.method == 'POST':
                    form = CourseTask.objects.create(
                        user = request.user,    
                        course = course,
                        title = title,
                        task = tag,
                        description = description,
                        body = body,
                        public = public
                    )
                    form.save()
                    
                    oneCourseTitle.tasks.add(form)
                    oneCourseTitle.save()
                    
                    return redirect('courses:tasks-panel', course.slug)
                
        elif tag == 'video':
            video = request.POST.get('video')
            oneCourseTitle = CourseTitle.objects.get(id=course_title)
            
            if validated:
                if request.method == 'POST':
                    form = CourseTask.objects.create(
                        user = request.user,    
                        course = course,
                        title = title,
                        task = tag,
                        description = description,
                        video = video,
                        public = public
                    )
                    form.save()
                    
                    oneCourseTitle.tasks.add(form)
                    oneCourseTitle.save()
                    
                    return redirect('courses:tasks-panel', course.slug)
    
    context = {'page': page, 'course': course, 'CourseTitles': CourseTitles} 
    return render(request, 'course/panel/coursePanel.html', context)

def updateTitle(request, slug, course_title_id):
    page = 'updateTitle'
    course = Course.objects.get(slug=slug)
    courseTitle = CourseTitle.objects.get(id=course_title_id)
    tasks = CourseTask.objects.filter(course=course)
    
    if request.method == 'POST':
        title = request.POST.get('title')
                
        if len(title) > 3:
            courseTitle.title = title
            # form.save()
            
            # return redirect('/courses/'+str(course.slug)+'/tasks-panel')
    
    context = {'page': page, 'course': course, 'courseTitle': courseTitle, 'tasks': tasks} 
    return render(request, 'course/panel/coursePanel.html', context)

def updateTask(request, slug, task_id):
    page = 'updateTask'
    course = Course.objects.get(slug=slug)
    task = CourseTask.objects.get(id=task_id)
    courseTitles = CourseTitle.objects.filter(course=course)
    TaskCourseTitle = CourseTitle.objects.filter()
    print(TaskCourseTitle)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tag = request.POST.get('tag')
        public = True
        
        validated = True
        
        if len(title) < 4:
            validated = False
            messages.error(request, 'Title must be at least 4 characters')
            
        if course == None or course == '':
            validated = False
            messages.error(request, 'Course is None')

        if tag == None or tag == '':
            validated = False
            messages.error(request, 'Tag is None')
  
        if validated:
            
            task.title = title
            task.task = tag
            task.description = description
            
            if tag == 'video':  
                task.video = request.POST.get('video')    
                
            elif tag == 'text':                
                task.body = request.POST.get('body')
              
            task.save()                
            
            return redirect('courses:tasks-panel', course.slug)
    
    
    context = {
        'page': page,
        'task': task, 
        'course': course, 
        'CourseTitles': courseTitles,
        # 'TaskCourseTitle': TaskCourseTitle,
    }
    return render(request, 'course/panel/coursePanel.html', context)

def deleteTitle(request, slug, title_id):
    page = 'deleteTitle'
    course = Course.objects.get(slug=slug)
    courseTitle = CourseTitle.objects.get(id=title_id)
    
    if request.method == 'POST':
        courseTitle.delete()
        return redirect('courses:tasks-panel', course.slug)
    
    context = {
        'page': page,
        'course': course,
        'courseTitle': courseTitle,
        # 'TaskCourseTitle': TaskCourseTitle,
    }
    return render(request, 'course/panel/coursePanel.html', context)

def deleteTask(request, slug, task_id):
    page = 'deleteTask'
    course = Course.objects.get(slug=slug)
    task = CourseTask.objects.get(id = task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('courses:tasks-panel', course.slug)
    
    context = {
        'page': page,
        'course': course,
        'courseTitle': task,
        # 'TaskCourseTitle': TaskCourseTitle,
    }
    return render(request, 'course/panel/coursePanel.html', context)

def ProfileComments(request, slug):
    page = 'comments'
    course = Course.objects.get(slug=slug)
    comments = CourseComment.objects.filter(course=course, commentType='comment')
    
    context = {
        'course': course,
        'page': page,
        'comments': comments,
    }
    return render(request, 'course/panel/coursePanel.html', context)

def ProfileReviews(request, slug):
    page = 'comments'
    course = Course.objects.get(slug=slug)
    comments = CourseComment.objects.filter(course=course, commentType='review')
    
    context = {
        'course': course,
        'page': page,
        'comments': comments,
    }
    return render(request, 'course/panel/coursePanel.html', context)