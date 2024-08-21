from typing import List

from django.contrib.auth.models import User

from apps.course.models import Course


def find_user_liked_courses(user: User) -> List[Course]:
    """
        Взятие курсов, что лайкнул пользователь

        :param user: User - Пользователь
        :return List[Course] - Список курсов
    """
    return Course.objects.filter(likes=user)