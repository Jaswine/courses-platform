from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_404_NOT_FOUND,
                                   HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from ..serializers.task_serializers import TaskOneSerializer
from ..services.course_service import get_course_by_id
from ..services.task_service import create_task, update_task, delete_task, add_remove_task_experience, \
    add_remove_task_bookmark, get_task_by_id
from ..services.title_service import get_course_title_by_id


@api_view(['POST'])
@permission_classes([IsAdminUser])
def task_create(request, id: int):
    """
        Создание задания
    """
    # Берем тему задания к курсу по его идентификатору
    course_title = get_course_title_by_id(id)
    if not course_title:
        return Response({'detail': f'Title with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем данные
    title = request.POST.get('title', '')
    task_type = request.POST.get('type', 'text')
    points = request.POST.get('points', 0)

    # Создаем таск
    task = create_task(course_title, title, task_type, points)

    # Проверяем, что таск создан успешно и выводи сообщение
    if task:
        return Response({'detail': 'The subject created successfully!'}, status=HTTP_201_CREATED)
    return Response({'detail': 'Task creation failed'}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def task_get_update_delete(request, id: int, task_id: int):
    """
        Вывод, обновление и удаление задания
    """
    # Берем курс по его идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем задание по его идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {task_id} not found.'}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskOneSerializer(task, many=False, context={'user': request.user})
        return JsonResponse(serializer.data, status=200)

    if not request.user.is_superuser:
        return Response({'detail': 'User does not have sufficient rights'}, status=HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':
            # Берем данные
            title = request.POST.get('task_title', '')
            public = request.POST.get('public', 'false')
            points = request.POST.get('points', 0)

            # Обновляем задание
            if update_task(task, title, public, points):
                return Response({'detail': 'Task updated successfully!'}, status=HTTP_200_OK)
            return Response({'detail': 'Task updation failed'}, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Удаляем задание
        delete_task(task)
        return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def task_add_experience(request, id: int, task_id: int):
    """
        Добавление / удаление опыта
    """
    # Берем курс по его идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем задание по его идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Добавляем или удаляем опыт к заданию
    message = add_remove_task_experience(task, request.user)
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def task_add_remove_bookmark(request, course_id: int, task_id: int):
    """
        Добавление / удаление из закладок
    """
    # Берем курс по его идентификатору
    course = get_course_by_id(course_id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем задание по его идентификатору
    task = get_task_by_id(task_id)
    if not task:
        return Response({'detail': f'Task with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Добавляем или удаляем закладку к заданию
    message = add_remove_task_bookmark(task, request.user)
    return Response({'detail': message}, status=HTTP_200_OK)
