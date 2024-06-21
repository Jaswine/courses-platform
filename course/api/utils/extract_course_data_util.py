from typing import List, Dict, Any

from django.contrib.auth.models import User

from course.models import CourseReview, Course


def generate_courses_list_util(user: User, courses: [Course]) -> list[
    dict[str, bool | None | list[dict[str, Any]] | Any]]:
    """
        Генерация списка с словарями данных курсов

        :param user: User                                             - Пользователь
        :param courses: [Course]                                      - Список курсов
        :return [dict[str, bool | None | list[dict[str, Any]] | Any]] - Список с словарями данных курсов
    """
    return [{
        'id': course.id,
        'title': course.title,
        'user': course.user.username,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in course.tags.all()],
        'image': course.image.url if course.image else None,
        'likes': course.likes.count(),
        'comments_count': CourseReview.objects.filter(course=course).count(),
        'liked_for_this_user': True if user in course.likes.all() else False,
        'updated': course.updated.strftime("%Y.%m.%d"),
        'created': course.created.strftime("%Y.%m.%d"),
    } for course in courses]