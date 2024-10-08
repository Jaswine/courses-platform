from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN)

from apps.course.api.serializers.task_comment_serializers import TaskCommentListSerializer, TaskCommentSerializer
from apps.course.api.services.cache_service import get_cache, set_cache, delete_cache_by_pattern
from apps.course.api.services.task_comment_service import create_task_comment, get_task_comment_by_id, \
    update_task_comment_parent, delete_task_comment, toggle_like_to_task_comment, filter_task_comment_user_complains, \
    save_task_comment_user_complain_form, get_comments_without_children_by_task
from apps.course.api.services.task_service import get_task_by_id
from apps.course.api.utils.validators_utils import full_number_validator
from apps.course.forms import TaskCommentUserComplaintForm
from django.core.paginator import Paginator
from django.conf import settings


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_comment_list_create(request, task_id: int):
    """
       Показ всех комментариев и создание нового комментария
    """
    if request.method == 'GET':
        page_number = full_number_validator(request.GET.get('page', 1))
        # Генерируем ключ для кэша на основе параметров запроса
        cache_key = f"course_task_comment_list_history_{task_id}_{page_number}"
        # Берем данные из кэша
        cache_data = get_cache(cache_key)
        if cache_data:
            return Response(cache_data, status=HTTP_200_OK)
        # Берем задание по идентификатору
        task = get_task_by_id(task_id)
        if not task:
            return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)
        # Берем комментарии
        comments = get_comments_without_children_by_task(task)
        # Добавляем пагинатор
        paginator = Paginator(comments, settings.PAGINATOR_PAGE_SIZE)
        page_obj = paginator.get_page(page_number)
        # Возвращаем список комментариев
        serializer = TaskCommentListSerializer(page_obj, many=True, context={'user': request.user})
        # Кешируем данные
        set_cache(cache_key, serializer.data, timeout=settings.COURSE_TASK_COMMENT_LIST_HISTORY)
        return Response({
            'page': page_number,
            'total': paginator.num_pages,
            'comments': serializer.data
        }, status=HTTP_200_OK)
    if request.method == 'POST':
        # Берем задание по идентификатору
        task = get_task_by_id(task_id)
        if not task:
            return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)
        # Берем данные
        message = request.data.get('message', '')
        parent_id = request.data.get('parent_id', None)
        # Проверяем длину сообщения
        if len(message) > 1000 or len(message) < 3:
            return Response({'detail': 'Message is too long!' if len(message) > 1000 else 'Message is too short!'},
                            status=HTTP_400_BAD_REQUEST)

        # Создаем новый комментарий
        new_task_comment = create_task_comment(task, request.user, message)
        # Проверяем, что передается id родителя и если передается, обновляем комментарий
        if parent_id:
            update_task_comment_parent(new_task_comment, get_task_comment_by_id(parent_id))
        # Удаляем весь кэш для пользователей
        delete_cache_by_pattern(f'course_task_comment_list_history_{task_id}')
        # Возвращаем комментарий
        comment_data = TaskCommentSerializer(new_task_comment, many=False, context={'user': request.user})
        return Response(comment_data.data, status=HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_comment_delete(request, task_id: int, comment_id: int):
    """
        Удаление комментария к заданию
    """
    # Берем задание по идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем комментарий по идентификатору
    comment = get_task_comment_by_id(comment_id)
    if not comment:
        return Response({'detail': f'Comment with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)
    # Проверяем, что текущий пользователь является создателем комментария
    if request.user != comment.user:
        return Response({'detail': 'You are not allowed to edit this comment.'}, status=HTTP_403_FORBIDDEN)
    # Удаление комментария
    delete_task_comment(comment)
    # Удаляем весь кэш для пользователей
    delete_cache_by_pattern(f'course_task_comment_list_history_{task_id}')
    return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def task_comment_add_remove_like(request, task_id: int, comment_id: int):
    """
        Реакция на комментарии
    """
    # Берем задание по идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем комментарий по идентификатору
    comment = get_task_comment_by_id(comment_id)
    if not comment:
        return Response({'detail': f'Comment with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Добавление или удаление лайка к заданию
    response_message = toggle_like_to_task_comment(comment, request.user)
    # Удаляем весь кэш для пользователей
    delete_cache_by_pattern('course_task_comment_list_history')
    return Response({'detail': response_message}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_comment_add_complaint(request, task_id: int, comment_id: int):
    """
        Оставление жалобы на комментарий
    """
    # Берем задание по идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем комментарий по идентификатору
    comment = get_task_comment_by_id(comment_id)
    if not comment:
        return Response({'detail': f'Comment with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Проверяем, что это первая запись пользователя
    comment_complaints = filter_task_comment_user_complains(comment, request.user)
    if comment_complaints.count() > 0:
        return Response({'detail': 'Complaint already exists!'}, status=HTTP_400_BAD_REQUEST)

    # Берем данные и создаем жалобу
    form = TaskCommentUserComplaintForm(request.data)
    response_message = save_task_comment_user_complain_form(comment, form, comment_complaints, request.user)

    # Выводим сообщение
    if 'Complaint added successfully' in response_message:
        return Response({'detail': response_message}, status=HTTP_201_CREATED)
    Response(form.errors, status=HTTP_400_BAD_REQUEST)


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
