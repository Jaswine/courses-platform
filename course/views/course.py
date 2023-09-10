from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Tag
from ..forms import CourseForm


@login_required(login_url='auth:sign-in')
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
    
