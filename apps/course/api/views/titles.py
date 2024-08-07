from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_404_NOT_FOUND,
                                   HTTP_400_BAD_REQUEST, HTTP_200_OK,
                                   HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from ..serializers.title_serializers import TitleListSerializer
from ..services.course_service import get_course_by_id
from ..services.title_service import create_course_title, delete_course_title, \
    filter_course_titles_by_id, get_course_title_by_id, update_course_title_name, update_course_title_public


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def title_list_create(request, id: int):
    """
        Вывод списка тем и создание новой темы
    """
    # Берем курс по идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Берем все темы
        titles = filter_course_titles_by_id(id)
        # Выводим темы
        serializer = TitleListSerializer(titles, many=True,
                                         context={'user': request.user, 'course': course})
        return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == 'POST':
        if request.user.is_superuser:
            # Берем данные
            title = request.POST.get('title', '')

            # Проверяем их
            if len(title) < 3 or 255 < len(title):
                return Response({'detail': 'The subject cannot be less than 0 or more than 255 characters'}, status=HTTP_400_BAD_REQUEST)

            # Создаем новую тему
            title = create_course_title(course, title)

            # Проверяем то, что тема создана успешно и выводим результат
            if title:
                return Response({'detail': 'Title created successfully'}, status=HTTP_201_CREATED)
            return Response({'detail': 'Title creation failed'}, status=HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You don\'n have enough permissions'}, status=HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def title_delete(request, title_id: int):
    """
        Удаление темы
    """
    # Берем задание к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Удаляем тему
    delete_course_title(course_title)
    return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def title_update_name(request, title_id: int):
    """
        Обновление названия темы
    """
    # Берем задание к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    title = request.POST.get('title', '')

    # Обновляем название темы
    message = update_course_title_name(course_title, title)
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def title_update_public(request, title_id: int):
    """
        Обновление публичности темы
    """
    # Берем задание к курсу по его идентификатору
    course_title = get_course_title_by_id(title_id)
    if not course_title:
        return Response({'detail': f'Title with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    public = request.POST.get('public', '')

    # Обновляем статус публичности темы
    message = update_course_title_public(course_title, public)
    return Response({'detail': message}, status=HTTP_200_OK)

# @api_view(['PATCH'])
# @permission_classes([IsAdminUser])
# def title_change_place(request, CourseID: int, TitleID: int, NewOrder: int):
#     # Берем курс по идентификатору
#     course = get_course_by_id(id)
#     if not course:
#         return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)
#
#     # Берем задание курса по его идентификатору
#     title = get_course_title_by_id(id)
#     if not title:
#         return Response({'detail': f'Title with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)
#
#
#         return Response({'detail': 'Title\' place changed successfully!'}, status=HTTP_200_OK)
#     return Response({'detail': 'New order not provided'}, status=HTTP_400_BAD_REQUEST)
