from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from course.models import Course, UserTaskProgress, Tag


def dashboard(request):
    if request.user.is_authenticated:
        courses = UserTaskProgress.objects.filter(user=request.user)
    
        context = {
            'courses': courses,
        }
        return render(request, 'auth/dashboard.html', context)
    else:
        tags = Tag.objects.filter(course__isnull=False).distinct()
        
        return render(request, 'auth/index.html', {
            'tags': tags,
        })

@login_required(login_url='auth:sign-in')
def favorites(request):
    courses = Course.objects.filter(likes=request.user)
    
    context = {
        'courses': courses,
    }
    return render(request, 'auth/lowers.html', context)

@login_required(login_url='auth:sign-in')
def courses(request):
    courses = UserTaskProgress.objects.filter(user=request.user, public=True)
    
    context = {
        'courses': courses,
    }
    return render(request, 'auth/dashboard.html', context)