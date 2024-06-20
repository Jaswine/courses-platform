from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from course.api.utils.get_element_or_404 import get_element_or_404
from course.models import Task, TaskComment
from user.models import Reaction


def task_comment_list_create(request, task_id: int):
    if request.user.is_authenticated:
        task = get_element_or_404(Task, task_id)

        if isinstance(task, JsonResponse):
            return task

        if request.method == 'GET':
            """
                Показ всех комментариев
            """
            comments = TaskComment.objects.prefetch_related("task_comment_children").filter(task=task,
                                                                                            task_comment_parent=None)
            comment_list = []

            # for comment in comments:
            #     data = dict()
            #     data['id'] = comment.id
            #     data['user'] = {
            #         'username': comment.user.username,
            #         'ava': comment.user.profile.image.url if comment.user.profile.image else None,
            #     }
            #     data['message'] = comment.text
            #     data['created'] = comment.created.strftime("%H:%M %d.%m.%Y")
            #     data['updated'] = comment.updated.strftime("%H:%M %d.%m.%Y")
            #
            #     data_reactions = dict(Reaction.REACTION_CHOICES)
            #     for reaction in comment.reactions.all():
            #         for choice in data_reactions.keys():
            #             if reaction.reaction_type == choice:
            #                 data_reactions[choice] = data_reactions[choice] + 1 if type(data_reactions[choice]) == int else 1
            #
            #     for reaction in data_reactions.keys():
            #         if type(data_reactions[reaction]) == str:
            #             data_reactions[reaction] = 0
            #
            #     my_data_reaction = comment.reactions.filter(user=request.user).first()
            #     data_reactions['MyReaction'] = my_data_reaction.reaction_type if my_data_reaction else None
            #
            #     data['reactions'] = data_reactions
            #
            #     comment_list.append(data)

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
