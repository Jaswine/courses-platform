from django.shortcuts import render, redirect
from django.contrib import messages 

# models
from .models import Tag, CourseTitle, Course, CourseComment, CourseTask

# services
from .services import course_filter, get_one_comment, course_title_filter, course_get_comments, get_one_comment, get_one_course, get_one_task, get_all_exercises_from_titles
from base.services import get_all_courses
from article.services import get_all_tags

# utils
from .utils import len_checking, slug_checking, isNotNone


def catalog(request):
    # get all courses
    courses = course_filter()
    
    context = {
        'courses': courses
    }
    return render(request, 'course/Catalog.html', context)

def course(request, slug):
    # get course and titles
    course = get_one_course(slug)
    titles = course_title_filter(course.id)
    reviews = course_get_comments(course, 'review')
    
    first_element = ""

    # get first element
    if (titles.count() != 0):
        first_element = titles[0].tasks.all()[0]
    
    # counts
    courseTitlesCount = titles.count()
    courseTasksCount = CourseTask.objects.filter(course = course).count()
    courseCommentsCount = reviews.count
    likes = course.likes.count
    
    commentPermission = True
    
    # review checked
    for i in reviews:  
        if i.user.username == request.user.username:
            commentPermission = False   

    liked = False

    for like in course.likes.all():
        if like.username == request.user.username:
            status = True 
            liked = True     

    if request.method == 'POST':
        if request.user.is_authenticated:
            # get type
            type = request.POST.get('type')

            # add likes
            if type == 'like':
                status = False
                
                for like in course.likes.all():
                    if like.username == request.user.username:
                        status = True      
                
                if status:
                    liked = False
                    course.likes.remove(like)
                else:
                    liked = True
                    course.likes.add(request.user)
                    course.save()

            # add review
            if type == 'review':
                # get data from form
                message = request.POST.get('message')
                stars = request.POST.get('stars')
                user = request.user

                if stars:
                    # create review
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
            return redirect('base:login')
                
    context = {
        'course': course, 
        'titles': titles,
        
        'courseTitlesCount': courseTitlesCount,
        'courseTasksCount': courseTasksCount,
        'courseCommentsCount': courseCommentsCount,
        
        'likes': likes,
        'liked': liked,
        'reviews': reviews,
        
        'commentPermission': commentPermission,
        
        'first_element': first_element,
    }
    return render(request, 'course/CourseInfo.html', context)

def deleteReview(request,slug, id):
    if request.user.is_authenticated:
        # get comment 
        comment =  get_one_comment(id)

        # delete comment
        if request.user.username == comment.user.username:
            comment.delete()
            return redirect('/courses/'+ str(slug)+'#reviews')
    else:
        return redirect('base:registration')

def task(request, slug, pk):
    # get courses and tasks
    course = get_one_course(slug=slug)
    task =  get_one_task(pk)
    titles = CourseTitle.objects.filter(course=course.id)
    comments = CourseComment.objects.filter(course=course, courseTask=task)
    
    # all tasks 
    tasks = get_all_exercises_from_titles(titles)
    prev_page = ''
    next_page = ''
    
    number = tasks.index(task)
    
    try: 
        if (tasks[number+1]):
            next_page = tasks[number+1]
    except:
        print('Error')
    
    try: 
        if (tasks[number-1] and  number!=0):
            prev_page = tasks[number-1]
    except:
        print('Error')
    
    if request.user.is_authenticated != True:
        return redirect('base:login')
    
    if request.method == 'POST':
        if (request.user.is_authenticated):
            # get data from form
            comment = request.POST.get('comment')
            
            # create a new Course
            form = CourseComment.objects.create(
                commentType = 'comment',
                course = course,
                user = request.user,
                message = comment,
                courseTask = task,
            )
            
            form.save()
            return redirect('courses:task', course.slug, task.id)
        else:
            return redirect('base:login')
    
    context = {
        'course': course,
        'task': task,
        
        'titles': titles,
        'tasks': tasks,
        
        'priv_page': prev_page,
        'next_page': next_page,
        
        'comments': comments
    }
    return render(request, 'course/Task.html', context)

def courseTaskCommentDelete(request, slug, pk, comment_id):
    if request.user.is_authenticated:
        # get course and task
        course = get_one_course(slug)
        task = CourseTask.objects.get(id=pk)
        courseComment = CourseComment.objects.get(id=comment_id)
        
        if courseComment:
            if request.user.username == courseComment.user.username:
                # delete the comment
                courseComment.delete()
                return redirect('courses:task', course.slug, task.id)    
            else: 
                messages.error(request, 'I think, u are not the author this comment')
        else:
            messages.error(request, 'comment not found')
    else:
        return redirect('base:registration')

def createCourse(request):
    if request.user.is_superuser:
        tags = get_all_tags()
        courses = get_all_courses()
        
        if request.method == 'POST':
            # get data
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

            validated = len_checking(about, 10)
            validated = len_checking(title, 6)
            validated = slug_checking(courses, slug)

            #! Tag Doesn't Selected
            validated = isNotNone(tag)      
                        
            if validated == True:
                tag = Tag.objects.get(id = tag)

                # Create Course   
                form = Course.objects.create(
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
    else:
        return redirect('base:registration')

def updateInfoPanel(request, slug):
    if request.user.is_superuser:
        page = 'UpdateInfoPanel'
        course = get_one_course(slug)
        courses = get_all_courses()
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
    else:
        return request('base:registration')

def TasksPanel(request, slug):
    if request.user.is_superuser:
        page = 'TasksPanel'
        course = get_one_course(slug)
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
    else:
        return redirect('base:registration')

def createTask(request, slug):
    if request.user.is_superuser:
        page = 'create_task'
        course = get_one_course(slug)
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
                messages.error(request, 'Task Type is None')
            
            if tag == 'text':
                body = request.POST.get('body')
                oneCourseTitle = CourseTitle.objects.get(id=course_title)
                
                if validated:
                    if request.method == 'POST':
                        form = CourseTask.objects.create(
                            user = request.user,    
                            course = course,
                            title = title,
                            taskType = tag,
                            description = description,
                            body = body,
                            public = public
                        )
                        form.save()
                        
                        oneCourseTitle.tasks.add(form)
                        oneCourseTitle.save()
                        
                        return redirect('courses:tasks-panel', course.slug)
                    
            elif tag == 'video':
                video = request.FILES.get('video', None)
                oneCourseTitle = CourseTitle.objects.get(id=course_title)
                
                if validated:
                    if request.method == 'POST':
                        print(video)

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
    else:
        return redirect('base:registration')

def updateTitle(request, slug, course_title_id):
    if request.user.is_superuser:
        page = 'updateTitle'
        course = get_one_course(slug)
        courseTitle = CourseTitle.objects.get(id=course_title_id)
        tasks = CourseTask.objects.filter(course=course)
        
        if request.method == 'POST':
            title = request.POST.get('title')

            validate = validate(title, 6)        
            
            if (validate):
                form.save()
                return redirect('/courses/'+str(course.slug)+'/tasks-panel')
        
        context = {'page': page, 'course': course, 'courseTitle': courseTitle, 'tasks': tasks} 
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')

def updateTask(request, slug, task_id):
    if request.user.is_superuser:
        page = 'updateTask'
        course = get_one_course(slug)
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
                task.taskType = tag
                task.description = description
                
                if tag == 'video':  
                    task.video = request.FILES.get('video')  
                    
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
    else:
        return redirect('base:registration')
    
def deleteTitle(request, slug, title_id):
    if request.user.is_superuser:
        page = 'deleteTitle'
        course = get_one_course(slug)
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
    else:
        return redirect('base:registration')

def deleteTask(request, slug, task_id):
    if request.user.is_superuser:
        page = 'deleteTask'
        course = get_one_course(slug)
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
    else:
        return redirect('base:registration')

def ProfileComments(request, slug):
    if request.user.is_superuser:
        page = 'comments'
        course = get_one_course(slug)
        comments = CourseComment.objects.filter(course=course, commentType='comment')
        
        context = {
            'course': course,
            'page': page,
            'comments': comments,
        }
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')

def ProfileReviews(request, slug):
    if request.user.is_superuser:
        page = 'comments'
        course = get_one_course(slug)
        comments = CourseComment.objects.filter(course=course, commentType='review')
        
        context = {
            'course': course,
            'page': page,
            'comments': comments,
        }
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')