from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Tag, Course

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
    print(course.tags.all())
    return render(request, 'course/course.html', {
        'course': course
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
        
        return render(request, 'course/edit_course.html', {
            'course': course,
            'form': form
        })
    else:
        messages.error(request, '')
        return redirect('/')
    
