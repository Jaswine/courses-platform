from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Tag, Course, Task, TaskOrder

from ..forms import CourseForm

def courses(request):
    return render(request, 'course/courses.html')

@login_required(login_url='auth:sign-in')
def create_course(request):
    if request.user.is_superuser:
        form = CourseForm()
        
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
           
            if form.is_valid():
                course = form.save(commit=False)
                course.user = request.user
            
                form.save()
                return redirect('/')
        
        return render(request, 'course/create_course.html', {
            'form': form
        })
    else:
        messages.error(request, '')
        return redirect('/')
    

def course(request, id):
    course = get_object_or_404(Course, pk=id)
    tasks = course.tasks.all().filter(public=True)
    
    videos_count = tasks.filter(type='video').count()    

    return render(request, 'course/course.html', {
        'course': course,
        'tasks': tasks,
        
        'videos_count': videos_count,
        'lessons_count': tasks.count(),
    })
    
    
@login_required(login_url='auth:sign-in')
def course_edit(request, id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        
        form = CourseForm(instance=course)
        
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES, instance=course)
           
            if form.is_valid():
                form.save()
                
                return redirect('course:course-edit', course.id)
        
        return render(request, 'course/edit/edit_course.html', {
            'course': course,
            'form': form
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
@login_required(login_url='auth:sign-in')
def course_delete(request, id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
                
        if request.method == 'POST':
            course.delete()
            messages.success(request, 'Course deleted successfully!')   
            return redirect('course:course')
        
        return render(request, 'course/delete_course.html', {
            'course': course,
            'url': '/courses'
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
@login_required(login_url='auth:sign-in')
def course_edit_tasks(request, id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        
        return render(request, 'course/edit/edit_course_tasks.html', {
            'course': course,
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
@login_required(login_url='auth:sign-in')
def course_task_create(request, id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        
        if request.method == 'POST':
            title = request.POST.get('title')
            type = request.POST.get('type')
            public = request.POST.get('public')
            
            if public == 'on':
                public = True
            else:
                public = False  
            
            task = Task.objects.create(title=title, 
                                           type=type,
                                           public=public)
            
            task.save()
            
            if type == 'text':
                task.text = request.POST.get('text')
                
            elif type == 'video':
                task.video = request.FILES.get('video') 
                
            task.save()            
                    
            order = course.tasks.count() + 1
            TaskOrder.objects.create(course=course, task=task, order=order)
            
            course.tasks.add(task)
            
            return redirect('course:course-edit-tasks', course.id)
            
        
        return render(request, 'course/edit/course_tasks_form.html', {
            'course': course,
        })
    else:
        messages.error(request, '')
        return redirect('/')

@login_required(login_url='auth:sign-in')
def course_task_update(request, id, task_id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        task = get_object_or_404(Task, pk=task_id)
        
        if request.method == 'POST':
            task.title = request.POST.get('title')
            
            type = request.POST.get('type')
            task.type = type
            print(type)
            
            public = request.POST.get('public')
            
            if public == 'on':
                task.public = True
            else:
                task.public = False  
            
            if type == 'text':
                task.text = request.POST.get('text')
                
            elif type == 'video':
                video = request.FILES.get('video')
                print(video)
                
                if video:
                    task.video = video
                
            task.save()            
            return redirect('course:course-edit-tasks', course.id)
        
        return render(request, 'course/edit/course_tasks_form.html', {
            'course': course,
            'task': task,
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
@login_required(login_url='auth:sign-in')
def course_task_delete(request, id, task_id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        task = get_object_or_404(Task, pk=task_id)
        
        if request.method == 'POST':
            task.delete()
            return redirect('course:course-edit-tasks', course.id)
        
        return render(request, 'course/delete_course.html', {
            'course': task,
            'url': f'/courses/{course.id}/edit/tasks'
        })
    else:
        messages.error(request, '')
        return redirect('/')
            