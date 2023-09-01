from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from course.models import Course, UserTaskProgress


@login_required(login_url='auth:sign-in')
def dashboard(request):
    courses = UserTaskProgress.objects.filter(user=request.user)
    
    context = {
        'courses': courses,
    }
    return render(request, 'auth/dashboard.html', context)

@login_required(login_url='auth:sign-in')
def courses(request):
    courses = UserTaskProgress.objects.filter(user=request.user, public=True)
    
    context = {
        'courses': courses,
    }
    return render(request, 'auth/dashboard.html', context)