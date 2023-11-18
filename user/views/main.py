from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from course.models import Course, Tag


def dashboard(request):
    if request.user.is_authenticated:
        courses_before_3 = request.user.users_who_registered.all()[:3]
        courses_after_3 = request.user.users_who_registered.all()[3:]
    
        context = {
            'courses_before_3': courses_before_3,
            'courses_after_3': courses_after_3,
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
    # courses = UserCourseProgress.objects.filter(user=request.user, public=True)
    
    context = {
        # 'courses': courses,
    }
    return render(request, 'auth/dashboard.html', context)