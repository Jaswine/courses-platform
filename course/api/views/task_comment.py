from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from course.api.utils.get_element_or_404 import get_element_or_404
from course.models import Task, TaskComment


def task_comment_list_create(request, task_id: int):
    if request.user.is_authenticated:
        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

        if request.method == 'GET':
            """
                Показ всех комментариев
            """
            comments = TaskComment.objects.prefetch_related("task_comment_children").filter(task=task, task_comment_parent=None)
            comment_list = [{
                'id': comment.id,
                'user': {
                    'username': comment.user.username,
                    'ava': comment.user.profile.image.url if comment.user.profile.image else None,
                },
                'message': comment.text,
                'updated': comment.updated.strftime("%H:%M %d.%m.%Y"),
                'created': comment.created.strftime("%H:%M %d.%m.%Y"),
            } for comment in comments]

            return JsonResponse({
                'status': 'success',
                'comments': comment_list,
            }, status=200)
        elif request.method == 'POST':
            """
               Создание нового комментария
           """
            message = request.POST.get('message')
            parent_id = request.POST.get('parent_id')

            if len(message) > 1000:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message is too long!'
                }, status=400)

            new_task_comment = TaskComment.objects.create(
                task=task,
                user=request.user,
                text=message,
            )

            if parent_id:
                new_task_comment.task_comment_parent = TaskComment.objects.get(id=parent_id)
                new_task_comment.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Comment created successfully!'
            }, status=201)
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed!'
        }, status=405)
    return JsonResponse({
        'status': 'error',
        'message': 'User is not authenticated!'
    }, status=401)


@csrf_exempt
def task_comment_update_delete(request, task_id: int, comment_id: int):
    """
        Удаление комментария к заданию
    """
    if request.user.is_authenticated:
        if request.method == 'DELETE':
            task = get_element_or_404(Task, task_id)

            if isinstance(task, JsonResponse):
                return task

            comment = TaskComment.objects.get(id=comment_id)

            if isinstance(comment, JsonResponse):
                return comment

            if request.user != comment.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This user is not allowed to delete this comment!'
                }, status=405)

            comment.delete()
            return JsonResponse({}, status=204)
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed!'
        }, status=405)
    return JsonResponse({
        'status': 'error',
        'message': 'User is not authenticated!'
    }, status=401)
