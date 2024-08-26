from typing import List

from django.contrib.auth.models import User
from django.db.models import Q

from apps.course.models import Course


def find_user_liked_courses(user: User) -> List[Course]:
    """
        Взятие курсов, что лайкнул пользователь

        :param user: User - Пользователь
        :return List[Course] - Список курсов
    """
    return Course.objects.filter(likes=user)


def find_user_registered_courses(user: User) -> List[Course]:
    """
        Взятие курсов, куда зарегестрировался пользователь

        :param user: User - Пользователь
        :return List[Course] - Список курсов
    """
    return Course.objects.filter(users_who_registered=user)


def find_all_users() -> List[User]:
    """
        Взятие всех пользователей

        :return: List[User] - Список пользователей
    """
    return User.objects.all()


def search_users(users: List[User], q: str) -> List[User]:
    """
        Поиск пользователей

        :param users: List[User] - Список пользователей
        :param q: str - Строка для поиска
        :return: List[User] - Список пользователей
    """
    return users.filter(Q(username__icontains=q) |
                        Q(first_name__icontains=q) |
                        Q(last_name__icontains=q) |
                        Q(email__icontains=q))


def filter_users_by_is_active(users: List[User], status: bool) -> List[User]:
    """
        Фильтраця пользователей по статусу активности

        :param users: List[User] - Список пользователей
        :param: status: bool - Статус
        :return: List[User] - Список пользователей
    """
    return users.filter(is_active=status)


def filter_users_by_is_superuser(users: List[User], status: bool) -> List[User]:
    """
        Фильтраця пользователей по статусу суперпользователя

        :param users: List[User] - Список пользователей
        :param: status: bool - Статус
        :return: List[User] - Список пользователей
    """
    return users.filter(is_superuser=status)


def sort_users(users: List[User], order_by: str) -> List[User]:
    """

        :param users: List[User] -  Список пользователей
        :param order_by: str - Тип сортировки
        :return: List[User] - Список пользователей
    """
    match order_by:
        case 'Newest':
            return users.order_by('-date_joined')
        case 'Oldest':
            return users.order_by('date_joined')
        case 'Many points':
            return users.order_by('-profile__scores')
        case 'Few points':
            return users.order_by('profile__scores')
        case _:
            return users


def filter_search_sort_users(search: str = '',
                             is_superuser: bool = None,
                             is_active: bool = None,
                             order_by: str = None) -> List[User]:
    """
        Фильтрация, поиск и сортировка пользователей

        :param search: str Строка для поиска
        :param is_superuser: bool Статус суперпользователя
        :param is_active: bool  Статус активности пользователя
        :param order_by: str  Тип сортировки
        :return: List[User]  Список пользователей
    """
    users  = find_all_users()

    if search and len(search) > 2:
        users = search_users(users, search)
    if is_active is not None and type(is_active) is bool:
        users = filter_users_by_is_active(users, status=is_active)
    if is_superuser is not None and type(is_superuser) is bool:
        users = filter_users_by_is_active(users, status=is_superuser)
    if order_by:
        users = sort_users(users, order_by)

    return users