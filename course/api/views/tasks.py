from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import Reaction
from ..services.TaskCommentService import get_comments_without_children_by_task
from ..utils.extract_comment_data_util import generate_comment_list_util
from ..utils.get_element_or_404 import get_element_or_404
from ...models import Title, Task, TaskOrder, Course, TaskComment


def task_create(request, id):
    if request.user.is_superuser:
        course_title = get_element_or_404(Title, id)

        if isinstance(course_title, JsonResponse):
            return course_title

        if request.method == 'POST':
            title = request.POST.get('title', '')
            type = request.POST.get('type', 'text')
            points = request.POST.get('points', 0)

            if 0 < len(title) < 255:
                task = Task.objects.create(
                    title=title,
                    type=type,
                    points=points,
                    public=False
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
            content = dict()

            # Task content
            if task.type == 'TaskText':
                content['text'] = task.text
            elif task.type == 'TaskVideo':
                content['video_path'] = task.video.url if task.video else None
            elif task.type == 'TaskProject':
                content['text'] = task.text

            # Comments
            comments = get_comments_without_children_by_task(task)
            comment_list = generate_comment_list_util(comments, request.user)

            return JsonResponse({
                'status': 'success',
                'data': {
                    'title': task.title,
                    'type': task.type,
                    'points': task.points,
                    'public': task.public,
                    'content': content,
                    'comments': comment_list,
                }
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


@csrf_exempt
def task_add_experiense(request, id: int, task_id: int):
    if request.user.is_authenticated:
        course = get_element_or_404(Course, id)

        if isinstance(course, JsonResponse):
            return course

        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

        if request.method == 'POST':
            if task.users_who_completed.filter(id=request.user.id).exists():
                task.users_who_completed.remove(request.user.id)
            else:
                task.users_who_completed.add(request.user.id)

            task.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Task updated successfully!'
            }, status=200)

        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed!'
        }, status=405)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not authenticated'
        }, status=403)
