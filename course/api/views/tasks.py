from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Title, Task, TaskOrder, Course
from ..utils import get_element_or_404


def task_create(request, id):
    if request.user.is_superuser:
        course_title = get_element_or_404(Title, id)

        if isinstance(course_title, JsonResponse):
            return course_title
        
        if request.method == 'POST':
            title = request.POST.get('title', '')
            type = request.POST.get('type','text')
            points = request.POST.get('points', 0)

            if 0 < len(title) < 255:
                task = Task.objects.create(
                    title = title,
                    type = type,
                    points = points,
                    public = False
                )
                task.save()
            
                order = course_title.tasks.count() + 1
                TaskOrder.objects.create(title=title, task=task, order=order)
                title.tasks.add(title)

                return JsonResponse({
                    'status': 'success',
                    'message': ' The subject created successfully!'
                }, status=201)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': ' The subject cannot be less than 0 or more than 255 characters.'
                }, status=400)
            
        else: 
            return JsonResponse({
                'status': 'error',
                'message': 'Method not allowed'
            }, status=402)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not a superuser'
        }, status=403)


@csrf_exempt
def task_get_update_delete(request, id, task_id):
    if request.user.is_superuser:
        course = get_element_or_404(Course, id)

        if isinstance(course, JsonResponse):
            return course

        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

        if request.method == 'GET':
            return JsonResponse({
                'title': task.title,
                'type': task.type,
                'points': task.points,
                'public': task.public
            }, status=200)

        if request.method == 'POST':
            title = request.POST.get('task_title', '')
            public = request.POST.get('public', None)
            points = request.POST.get('points', None)

            if 0 < len(title) < 255:
                task.title = title
                is_changed = True
                task.save()

            if public:
                if public == 'true':
                    task.public = False
                else:
                    task.public = True
                is_changed = True
                task.save()

            if points:
                task.points = points
                is_changed = True
                task.save()

            if is_changed:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Task updated successfully!'
                }, status=200)
            else:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Task didn\'t change!'
                }, status=200)
        if request.method == 'DELETE':
            task.delete()

            return JsonResponse({}, status=204)

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Method not allowed'
            }, status=402)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not a superuser'
        }, status=403)