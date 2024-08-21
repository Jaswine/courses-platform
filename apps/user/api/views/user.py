from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from apps.course.api.serializers.course_serializers import CourseSerializer, CourseListSerializer, \
    CourseProgressSerializer
from apps.user.api.serializers.user_serializers import UserSerializer, ProfileSerializer
from apps.user.api.services.user_service import find_user_liked_courses, find_user_registered_courses
from apps.user.services.user_service import get_user_by_username


class UserInfoView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, username: str, info_type: str):
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