from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.models import Course, Tag


def dashboard(request):
    if request.user.is_authenticated:
        courses = []

        for course in Course.objects.all():
            if len(courses) < 3:
                if request.user in course.users_who_registered.all():
                    courses.append(course)

        return render(request, 'auth/dashboard.html', {
            'courses': courses,
        })
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