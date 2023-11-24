from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ...models import Title, Task, TaskOrder
from ..utils import get_element_or_404


def title_create(request, id):
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
                    points = points
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