from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from course.api.utils.get_element_or_404 import get_element_or_404
from course.forms import TaskCommentUserComplaintForm
from course.models import Task, TaskComment, TaskCommentUserComplaint
from user.models import Reaction


@require_http_methods(["POST"])
def task_comment_create(request, task_id: int):
    """
       Создание нового комментария
    """
    if request.user.is_authenticated:
        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

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

        comment_data = dict()
        comment_data['id'] = new_task_comment.id
        comment_data['user'] = {
            'username': new_task_comment.user.username,
            'ava': new_task_comment.user.profile.image.url if new_task_comment.user.profile.image else None,
        }
        comment_data['likes'] = {
            'count': new_task_comment.likes.count(),
            'my': True if request.user in new_task_comment.likes.all() else False,
        }
        comment_data['message'] = new_task_comment.text
        comment_data['created'] = new_task_comment.created.strftime("%H:%M %d.%m.%Y")
        comment_data['updated'] = new_task_comment.updated.strftime("%H:%M %d.%m.%Y")

        return JsonResponse({
            'status': 'success',
            'message': 'Comment created successfully!',
            'comment': comment_data,
        }, status=201)
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
            comment = TaskComment.objects.get(id=comment_id)

            if request.user != comment.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This user is not allowed to delete this comment!'
                }, status=403)

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


@csrf_exempt
@require_http_methods(["POST"])
def task_comment_add_remove_like(request, task_id: int, comment_id: int):
    """
        Реакция на комментарии
    """
    if request.user.is_authenticated:
        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

        comment = get_element_or_404(TaskComment, comment_id)

        if isinstance(comment, JsonResponse):
            return comment

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

        comment.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Like added successfully!' if request.user in comment.likes.all() else 'Like removed successfully!'
        }, status=200)
    return JsonResponse({
        'status': 'error',
        'message': 'User is not authenticated!'
    }, status=401)


@require_http_methods(["POST"])
def task_comment_add_complaint(request, task_id: int, comment_id: int):
    """
        Оставление жалобы на комментарий
    """
    if request.user.is_authenticated:
        task = get_object_or_404(Task, id=task_id)
        comment = get_object_or_404(TaskComment, id=comment_id)

        comment_complaints = TaskCommentUserComplaint.objects.filter(user=request.user)

        if comment_complaints.count() > 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Complaint already exists!'
            }, status=400)

        form = TaskCommentUserComplaintForm(request.POST)
        if form.is_valid() and comment_complaints.count() == 0:
            complaint = form.save(commit=False)
            complaint.taskComment = comment
            complaint.user = request.user
            complaint.save()

            if comment.complaints.count() >= 10:
                comment.is_public = False
                comment.save()

                return JsonResponse({
                    'status': 'success',
                    'message': 'Complaint added successfully! The message was hidden as complaints became 10 or more!'
                }, status=201)

            return JsonResponse({
                'status': 'success',
                'message': 'Complaint added successfully!'
            }, status=201)
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'User is not authenticated!'
    }, status=401)

# @require_http_methods(["POST"])
# def task_comment_react(request, task_id: int, comment_id: int):
#     """
#         Реакция на комментарии
#     """
#     if request.user.is_authenticated:
#
#         task = get_element_or_404(Task, task_id)
#
#         if isinstance(task, JsonResponse):
#             return task
#
#         comment = TaskComment.objects.get(id=comment_id)
#
#         if isinstance(comment, JsonResponse):
#             return comment
#
#         if request.user != comment.user:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'This user is not allowed to delete this comment!'
#             }, status=403)
#
#         print(request.POST)
#         reaction_type = request.POST.get('reaction_type')
#
#         if reaction_type not in dict(Reaction.REACTION_CHOICES).keys():
#             return JsonResponse({
#                 'status': 'error',
#                 'message': f'Invalid reaction type! {reaction_type} not found!'
#             }, status=400)
#
#         existing_reaction = comment.reactions.filter(user=request.user).first()
#
#         if existing_reaction:
#             if existing_reaction.reaction_type == reaction_type:
#                 # If the reaction is the same as the existing one, remove it
#                 comment.reactions.remove(existing_reaction)
#                 existing_reaction.delete()
#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'Reaction removed!'
#                 }, status=200)
#             else:
#                 # If the reaction is different, update it
#                 existing_reaction.reaction_type = reaction_type
#                 existing_reaction.save()
#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'Reaction updated!'
#                 }, status=200)
#         else:
#             # If there is no existing reaction, add a new one
#             new_reaction = Reaction.objects.create(user=request.user, reaction_type=reaction_type)
#             comment.reactions.add(new_reaction)
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Reaction added!'
#             }, status=201)
#     return JsonResponse({
#         'status': 'error',
#         'message': 'User is not authenticated!'
#     }, status=401)
