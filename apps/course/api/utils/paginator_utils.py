from django.conf import settings
from django.core.paginator import Paginator

from apps.course.models import Course


def create_paginator(courses: list[Course] = list, /, *, page: int = 1) -> list:
    """
        Создание пагинатора

        :param courses: list[Course] - Список курсов
        :param page: int - Страница
        :return Курсы
    """
    paginator = Paginator(courses, settings.PAGINATOR_PAGE_SIZE)
    return paginator.get_page(page)
