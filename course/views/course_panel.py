from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

# models
from ..models import Tag, Course, CourseTitle, Course, CourseTask

from ..forms import CourseForm, TaskForm

# services
from ..services import course_filter, get_one_course


@login_required(login_url='base:login')
def course_panel_tasks_view(request, slug):
    if request.user.is_superuser:
        page = 'TasksPanel'
        course = Course.objects.get(slug=slug)
        
        if request.method == 'POST':
            title = request.POST.get('title')
            
            if len(title) > 3:
                form = CourseTitle.objects.create(
                    title=title,
                    public = True,
                    user = request.user
                )
                course.course_titles.add(form.id)
                        
        context = {
            'page': page, 
            'course': course, 
        } 
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def course_panel_update_title_view(request, slug, title_id):
    if request.user.is_superuser:
        page = 'UpdateTasksPanel'
        course = Course.objects.get(slug=slug)
        course_title = CourseTitle.objects.get(id=title_id)
        course_tasks = CourseTask.objects.all()
        
        if request.method == 'POST':
            get_title = request.POST.get('title')
            tasks = [int(i) for i in request.POST.getlist('tasks')]
            
            course_title.title = get_title
            
            for task in tasks:
                course_title.tasks.add(task)
            
            course_title.save()
            return redirect('course:tasks-panel', course.slug)
                        
        context = {
            'page': page, 
            'course': course, 
            'title': course_title,
            'tasks': course_tasks, 
        } 
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def course_panel_update_info(request, slug):
    if request.user.is_superuser:
        page = 'UpdateInfoPanel'
        course = Course.objects.get(slug=slug)
        form = CourseForm(instance=course)
        
        if request.user.username == course.user.username:
            if request.method == 'POST':
                form = CourseForm(request.POST, request.FILES, instance=course)
                
                if form.is_valid():
                    form.save()
                    return redirect('course:course', slug)
        else:
           messages.error(request, 'U don\'t have some permissions')
        
        context = {
            'page': page, 
            'course': course, 
            'form': form,
        }
        return render(request, 'course/panel/coursePanel.html',context)  
    else:
        return request('base:registration')
    

    
@login_required(login_url='base:login')
def create_task_view(request, slug):
    if request.user.is_superuser:
        page = 'create_task'
        
        course = Course.objects.get(slug=slug)
        form = TaskForm()
        
        if request.method == 'POST':
            form = TaskForm(request.POST)
            tag = request.POST.get('tag')
            course_title_get = request.POST.get('course_title')
            
            if form.is_valid():
                task = form.save(commit=False)
                task.taskType = tag
                task.user = request.user
                
                course_title = CourseTitle.objects.get(id=int(course_title_get))
                course_title.tasks.add(task.id)
                course_title.save()
                
                if tag == 'video':
                    video = request.FILES.get('video', None)
                    task.video = video
                    task.save()
                    return redirect('course:create-task', course.slug)
                
                elif tag == 'text':
                    body = request.POST.get('body')
                    task.body = body
                    
                    task.save()
                    return redirect('course:tasks-panel', course.slug)
        
        context = {
            'page': page, 
            'course': course, 
            'form': form
        } 
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def update_task_view(request, slug, task_id):
    if request.user.is_superuser:
        page = 'updateTask'
        
        course = Course.objects.get(slug=slug)
        task = CourseTask.objects.get(id=task_id)
        
        form = TaskForm(instance=task)
        
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            tag = request.POST.get('tag')
            course_title_get = request.POST.get('course_title')
            
            if form.is_valid():
                task = form.save(commit=False)
                task.taskType = tag
                task.user = request.user
                
                course_title = CourseTitle.objects.get(id=int(course_title_get))
                course_title.tasks.add(task.id)
                
                if tag == 'video':
                    video = request.FILES.get('video', None)
                    task.video = video
                    task.save()
                    return redirect('course:create-task', course.slug)
                
                elif tag == 'text':
                    body = request.POST.get('body')
                    task.body = body
                    
                    task.save()
                    return redirect('course:tasks-panel', course.slug)
        
        context = {
            'page': page, 
            'course': course, 
            'form': form,
            'task': task
        } 
        return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def delete_task_view(request, slug, task_id):
    if request.user.is_superuser:
        page = 'deleteTask'
        
        course = Course.objects.get(slug=slug)
        task = CourseTask.objects.get(id=task_id)
            
        if request.user.username ==course.user.username:
            if request.method == 'POST':
                task.delete()
                return redirect('course:tasks-panel', course.slug)
            
            context = {
                'page': page, 
                'course': course, 
                'task': task
            } 
            return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def delete_title_view(request, slug, title_id):
    if request.user.is_superuser:
        page = 'deleteTitle'
        
        course = Course.objects.get(slug=slug)
        title = CourseTitle.objects.get(id=task_id)
            
        if request.user.username == course.user.username:
            if request.method == 'POST':
                title.delete()
                return redirect('course:tasks-panel', course.slug)
            
            context = {
                'page': page, 
                'course': course, 
                'task': title
            } 
            return render(request, 'course/panel/coursePanel.html', context)
    else:
        return redirect('base:registration')