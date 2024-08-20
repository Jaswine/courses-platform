from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from ..serializers.course_review_serializers import CourseReviewListSerializer
from ..serializers.course_serializers import CourseListSerializer, CourseOneSerializer, CreateCourseSerializer
from ..services.course_review_service import get_course_reviews, filter_course_reviews_by_user, create_course_review, \
    delete_course_review, get_course_review_by_id
from ..services.course_service import find_courses_by_user_status, search_courses, filter_courses_by_tags, sort_courses, \
    add_remove_like_to_course, add_remove_registration_to_course, get_course_by_id
from ..utils.calculate_median_stars_util import calculate_median_stars_util
from ..utils.course_utils import create_course_by_serializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def courses_list(request):
    """
        Список курсов и создание нового курса
    """
    if request.method == 'GET':
        # Берем параметры для фильтрации и сортировки
        query = request.GET.get('q', '')
        order_by_date = request.GET.get('order_by_data', '')
        filter_by_tag = request.GET.get('filter_by_tag', '')

        # Ищем курсы по статусу пользователя
        courses = find_courses_by_user_status(request.user)
        # Ищем курсы
        courses = search_courses(query, courses)
        # Фильтруем курсы по тэгам
        courses = filter_courses_by_tags(filter_by_tag.split(','), courses)
        # Сортируем курсы
        courses = sort_courses(order_by_date, courses)
        # Возвращаем курсы
        serializer = CourseListSerializer(courses, many=True, context={'user': request.user})
        return Response(serializer.data, status=HTTP_200_OK)
    if request.method == 'POST':
        data, errors = create_course_by_serializer(request.data, request.user)
        if errors:
            return Response(errors, status=HTTP_400_BAD_REQUEST)
        return Response({'message': 'Course created successfully!'}, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def courses_get(request, id: int):
    """
        Показ информации курса по идентификатору
    """
    # Берем курс по идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)
    # Возвращаем курс
    serializer = CourseOneSerializer(course, many=False, context={'user': request.user})
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def course_add_remove_like(request, id: int):
    """
        Добавление и удаление лайка к курсу
    """
    # Берем курс по идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Добавляем или удаляем лайк для курса
    message = add_remove_like_to_course(course, request.user)
    # Возвращаем сообщение
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def course_add_remove_user(request, id: int):
    """
        Регистрация и удаление пользователя с курса
    """
    # Берем курс по идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Регистрируем или удаляем текущего пользователя с курса
    message = add_remove_registration_to_course(course, request.user)
    # Возвращаем сообщение
    return Response({'detail': message}, status=HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def course_review_create_list(request, id):
    """
        Вывод всех отзывов и создание нового
    """
    # Берем курс по идентификатору
    course = get_course_by_id(id)
    if not course:
        return Response({'detail': f'Course with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Берем все отзывы для конкретного курса
        reviews = get_course_reviews(course)
        # Вычисляем среднюю оценку курса
        medium__stars = calculate_median_stars_util(reviews)

        # Выводим отзывы
        serializer = CourseReviewListSerializer(reviews, many=True)
        return Response({
            'reviews': serializer.data,
            'medium__stars': medium__stars,
        }, status=HTTP_200_OK)
    elif request.method == 'POST':
        # Проверяем, что у пользователя не создан отзыв
        if filter_course_reviews_by_user(course, request.user).count() != 0:
            return Response({'detail': 'Review already exists!'}, status=HTTP_400_BAD_REQUEST)

        # Берем данные
        message = request.POST.get('message', '')
        stars_count = request.POST.get('stars_count', 0)

        # Валидируем данные
        if not (1 <= stars_count <= 5) or not message or len(message) < 6:
            return Response({'detail': 'The problem of creating a review'}, status=HTTP_400_BAD_REQUEST)

        # Создаем отзыв
        create_course_review(course, request.user, message, stars_count)
        # Возвращаем сообщение об успехе
        return Response({'detail': 'Review created successfully'}, status=HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def course_reviews_delete(request, id):
    """
        Удаление отзыва
    """
    # Берем отзыв к курсу по идентификатору
    review = get_course_review_by_id(id)
    if not review:
        return Response({'detail': f'Course review with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    # Проверяем, что текущий пользователь тот же, что и тот, кто создал отзыв
    if request.user.id == review.user.id:
        # Удаляем отзыв
        delete_course_review(review)
        return Response({'detail': f'Review with id {id} deleted successfully'}, status=HTTP_204_NO_CONTENT)
    return Response({'detail': 'User does not have sufficient rights'}, status=HTTP_403_FORBIDDEN)
