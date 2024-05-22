from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Profile
from course.models import Task, TaskOrder
from ..forms import UpdateUserForm, UpdateProfileForm


@login_required(login_url='auth:sign-in')
def settings(request):
    profile = get_object_or_404(Profile, user=request.user)
    formUser = UpdateUserForm(instance=request.user)
    formProfile = UpdateProfileForm(instance=profile)

    if request.method == 'POST':
        formUser = UpdateUserForm(request.POST, instance=request.user)
        formProfile = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if formUser.is_valid() and formProfile.is_valid():
            formUser.save()
            formProfile.save()

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('auth:dashboard')
        else:
            messages.error(request, 'Something went wrong. Please try again.')
            return redirect('auth:settings')

    return render(request, 'auth/settings.html', {
        'formUser': formUser,
        'formProfile': formProfile,
    })

def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    courses = []
    courses_base = user.users_who_registered.all()
    
    for course in courses_base:
        completed_tasks_count = 0
        status = ''
        task_orders = TaskOrder.objects.filter(course_id=course.id).order_by('order')
        tasks = [task_order.task for task_order in task_orders]
        
        for task in tasks:
            if user in task.users_who_completed.all():
                completed_tasks_count += 1
                
        if completed_tasks_count == 0:
            status = 'Began'
        elif completed_tasks_count == len(tasks):
            status = 'Completed'
        else:
            status = 'Progress'
        
        courses.append({
            'id': course.id,
            'title': course.title,
            'points_earned': completed_tasks_count,
            'points_all': len(tasks),
            'status': status,
        })
    
    return render(request, 'auth/profile.html', {
        'user': user,
        'profile': profile,
        'courses': courses,
        'status': 'profile',
    })
    
def certificates(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    return render(request, 'auth/profile.html', {
        'user': user,
        'profile': profile,
        'status': 'certificates',
    })