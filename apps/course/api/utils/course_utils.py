from typing import Dict, List

from apps.course.api.serializers.course_serializers import CreateCourseSerializer
from apps.course.models import Course
from apps.user.models import User


def create_course_by_serializer(data: dict, user: User) -> (Dict | None, List | None):
    """
        Создаем новый курс с помощью сериалайзера

        :param data: Dict - Данные
        :param course: Course - Курс
    """
    serializer = CreateCourseSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return serializer.data, None
    return None, serializer.errors


def update_course_by_serializer(course: Course, data) -> (Dict | None, List | None):
    """
        Обновляем данные курса с помощью сериалайзера

        :param course: Course - Курс
        :param data: Dict - Данные
    """
    serializer = CreateCourseSerializer(instance=course, data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data, None
    return None, serializer.errors
