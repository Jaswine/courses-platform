from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from course.models import Course, Tag


def dashboard(request):
    """
        Панель управления
    """
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
    """
        Лайкнутые курсы и статьи
    """
    return render(request, 'auth/lowers.html')
