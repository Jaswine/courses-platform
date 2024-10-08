from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_404_NOT_FOUND,
                                   HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from ..serializers.title_serializers import TitleListSerializer
from ..services.cache_service import get_cache, set_cache, delete_cache_by_pattern
from ..services.course_service import get_course_by_id
from ..services.title_service import create_course_title, delete_course_title, \
    filter_course_titles_by_id, get_course_title_by_id, update_course_title_name, update_course_title_public, \
    update_titles_places


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def title_list_create(request, course_id: int):
    """
        Вывод списка тем и создание новой темы
    """
    if request.method == 'GET':
        # Генерируем ключ для кэша на основе параметров запроса
        cache_key = f"course_titles_and_tasks_list_history_{course_id}_{request.user.username}"
        # Берем данные из кэша
        cache_data = get_cache(cache_key)
        if cache_data:
            return Response(cache_data, status=HTTP_200_OK)
        # Берем курс по идентификатору
        course = get_course_by_id(course_id)
        if not course:
            return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)
        # Берем все темы
        titles = filter_course_titles_by_id(course_id)
        serializer = TitleListSerializer(titles, many=True,
                                         context={'user': request.user, 'course': course})
        # Кешируем данные
        set_cache(cache_key, serializer.data, timeout=settings.COURSE_TITLE_AND_TASK_LIST_CACHE_TIMEOUT)
        return Response(serializer.data, status=HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.is_superuser:
            # Берем курс по идентификатору
            course = get_course_by_id(course_id)
            if not course:
                return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)
            # Берем данные
            title = request.data.get('title')
            # Проверяем их
            if len(title) < 3 or 255 < len(title):
                return Response({'detail': 'The subject cannot be less than 0 or more than 255 characters'}, status=HTTP_400_BAD_REQUEST)
            # Создаем новую тему
            title = create_course_title(course, title)
            # Удаляем весь кэш для пользователей
            delete_cache_by_pattern(f'course_titles_and_tasks_list_history_{course_id}')
            # Проверяем то, что тема создана успешно и выводим результат
            if title:
                return Response({'detail': 'Title created successfully'}, status=HTTP_201_CREATED)
            return Response({'detail': 'Title creation failed'}, status=HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You don\'n have enough permissions'}, status=HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def title_delete(request, course_id: int, title_id: int):
    """
        Удаление темы
    """
    # Берем курс по идентификатору
    course = get_course_by_id(course_id)
    if not course:
        return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем задание к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {title_id} not found.'}, status=HTTP_404_NOT_FOUND)
    # Удаляем тему
    delete_course_title(course_title)
    # Удаляем весь кэш для пользователей
    delete_cache_by_pattern(f'course_titles_and_tasks_list_history_{course_id}')
    return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def title_update_name(request, course_id: int, title_id: int):
    """
        Обновление названия темы
    """
    # Берем курс по идентификатору
    course = get_course_by_id(course_id)
    if not course:
        return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем задание к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {title_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем новое название темы и проверяем его
    title = request.data.get('title', '')
    if len(title) < 3 or 255 < len(title):
        return Response({'detail': 'The subject cannot be less than 0 or more than 255 characters'},
                        status=HTTP_400_BAD_REQUEST)

    # Обновляем название темы
    message = update_course_title_name(course_title, title)
    # Удаляем весь кэш для пользователей
    delete_cache_by_pattern(f'course_titles_and_tasks_list_history_{course_id}')
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def title_update_public(request, course_id: int, title_id: int):
    """
        Обновление публичности темы
    """
    # Берем курс по идентификатору
    course = get_course_by_id(course_id)
    if not course:
        return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем тему к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {title_id} not found.'}, status=HTTP_404_NOT_FOUND)

    public = request.data.get('public')
    # Проверяем
    if public: return Response({'detail': 'Public not found'}, status=HTTP_400_BAD_REQUEST)
    # Обновляем статус публичности темы
    message = update_course_title_public(course_title, public)
    # Удаляем весь кэш для пользователей
    delete_cache_by_pattern(f'course_titles_and_tasks_list_history_{course_id}')
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def title_change_titles_place(request, course_id: int, title1_id: int, title2_id: int):
    """
        Смена тем местами
    """
    # Берем курс по идентификатору
    course = get_course_by_id(course_id)
    if not course:
        return Response({'detail': f'Course with ID: {course_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем первую тему курса по ее идентификатору
    course_title1 = get_course_title_by_id(title1_id)
    if not course_title1:
        return Response({'detail': f'The first title with ID: {title1_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Берем вторую тему курса по ее идентификатору
    course_title2 = get_course_title_by_id(title2_id)
    if not course_title2:
        return Response({'detail': f'The second title with ID: {title2_id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Обновляем данные
    if update_titles_places(course, course_title1, course_title2):
        # Удаляем весь кэш для пользователей
        delete_cache_by_pattern(f'course_titles_and_tasks_list_history_{course_id}')
        return Response({'detail': 'Title\'s order changed successfully!'}, status=HTTP_200_OK)
    return Response({'detail': 'Title\'s order changed failed'}, status=HTTP_400_BAD_REQUEST)
