from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, IsAdminUser)

from apps.course.api.serializers.course_serializers import CourseListSerializer, CourseProgressSerializer
from apps.user.api.serializers.user_serializers import UserSerializer, ProfileSerializer
from apps.user.api.services.user_service import (find_user_liked_courses,
                                                 find_user_registered_courses, filter_search_sort_users)
from apps.user.services.user_service import get_user_by_username


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_list(request):
    q = request.GET.get('q')
    is_superuser = request.GET.get('is_superuser')
    is_active = request.GET.get('is_active')
    order_by = request.GET.get('order_by')

    users = filter_search_sort_users(q, is_superuser, is_active, order_by)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_view(request, username: str, info_type: str):
    # Взятие пользователя
    user = get_user_by_username(username)
    if user is None:
        return Response({'detail': f'User with username: {username} not found.'},
                        status=HTTP_404_NOT_FOUND)

    if info_type == 'main':
        # Главная информация о пользователе
        serializer = UserSerializer(user, many=False)
    elif info_type == 'detail':
        # Детальная информация о пользователе
        serializer = ProfileSerializer(user.profile, many=False)
    elif info_type == 'liked-courses':
        # Лайкнутые курсы
        courses = find_user_liked_courses(user)
        serializer = CourseListSerializer(courses, many=True)
    elif info_type == 'courses-progress':
        # Прогресс по курсам
        courses = find_user_registered_courses(user)
        serializer = CourseProgressSerializer(courses, many=True,
                                              context={'user': user})
    else:
        return Response({"detail": "Page not found"}, status=HTTP_404_NOT_FOUND)

    return Response(serializer.data, status=HTTP_200_OK)

