from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Tag, Course, Task, TaskOrder, Title, TitleOrder

from ..forms import CourseForm, TaskForm

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
                course.save()
                return redirect('/')
            else:
                messages.error(request, 'Form is not valid')
        
        return render(request, 'course/create_course.html', {
            'form': form
        })
    else:
        messages.error(request, '')
        return redirect('/')
    

def course(request, id):
    course = get_object_or_404(Course, pk=id)
    
    return render(request, 'course/course.html', {
        'course': course,
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
def course_task_create(request, id, title_id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        course_title = get_object_or_404(Title, pk=title_id)
        form = TaskForm()
        
        if request.method == 'POST':
            form = TaskForm(request.POST)

            if form.is_valid():
                type = request.POST.get('type')
                public = request.POST.get('public')
                points = request.POST.get('points')
                
                if public == 'on':
                    public = True
                else:
                    public = False  
                
                task = Task.objects.create(title=form.cleaned_data['title'], 
                                            type=type,
                                            public=public,
                                            points=points)
                
                task.save()

                order = course_title.tasks.count() + 1
                TaskOrder.objects.create(title=course_title, task=task, order=order)
            
                course_title.tasks.add(task)
                course_title.save()
                
                if type == 'TaskText':
                    task.text = form.cleaned_data['text']
                elif type == 'TaskVideo':
                    task.text = form.cleaned_data['text']
                    task.video = request.FILES.get('video') 
                elif type == 'TaskProject':
                    task.text = form.cleaned_data['text']
                elif type == 'TaskQuestions':
                    messages.error(request, 'This task\'s type not supported!')
                elif type == 'TaskQuestions':
                    messages.error(request, 'This task\'s type not supported!')
                    
                task.save()            
                return redirect('course:course-edit-tasks', course.id)
            
        return render(request, 'course/edit/course_tasks_form.html', {
            'course': course,
            'form': form,
        })
    else:
        messages.error(request, '')
        return redirect('/')

@login_required(login_url='auth:sign-in')
def course_task_update(request, id, task_id):    
    if request.user.is_superuser:
        course = get_object_or_404(Course, pk=id)
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)

            if form.is_valid():
                form.save(commit=False)

                task.type = request.POST.get('type')
                task.points = request.POST.get('points')

                public = request.POST.get('public')
            
                if public == 'on':
                    task.public = True
                else:
                    task.public = False

                if type == 'video':
                    video = request.FILES.get('video')

                    if video:
                        task.video = video

                task.save()
                form.save()
                return redirect('course:course-edit-tasks', course.id)
        
        return render(request, 'course/edit/course_tasks_form_edit.html', {
            'course': course,
            'task': task,
            'form': form,
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
@login_required(login_url='auth:sign-in')
def course_task_delete(request, id: int, task_id: int):
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


@login_required(login_url='auth:sign-in')
def course_task(request, id: int, task_id: int):
    course = get_object_or_404(Course, pk=id)
    task = get_object_or_404(Task, pk=task_id)
    
    return render(request, 'course/task.html', {
        'task': task,
        'course': course,
    })