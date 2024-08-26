from django.contrib.auth.models import User
from django.db.models import Q, Count

from apps.course.models import Course, Tag


def get_all_courses() -> list[Course]:
    """
        Вывод всех курсов

        :return list[Course]  - список курсов
    """
    return Course.objects.all()


def get_course_by_id(course_id: int) -> Course | None:
    """
       Взятие курса по идентификатору

       :param course_id: int   - Идентификатор курса
       :return Course | None   - Курс
    """
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return None


def find_courses_by_user_status(user_status: bool) -> list[Course]:
    """
        Взятие курсов взависимости от типа пользователя

        :param user_status: bool  - статус пользователя
        :return [Course] - список курсов
    """
    return get_all_courses() if user_status else Course.objects.filter(user_status=user_status)


def search_courses(query: str, courses: list[Course]) -> list[Course]:
    """
        Поиск курсов

        :param query: str              - строка для поиска
        :param courses: list[Course]   - список курсов
        :return list[Course]       - список курсов
    """
    return courses.filter(Q(title__icontains=query))


def filter_courses_by_tags(tags: [Tag], courses: list[Course]) -> list[Course]:
    """
        Фильтрация курсов по списку

        :param  tags: [Tag]               - строка для фильтрации по тегам
        :param  courses: list[Course]     - список курсов
        :return list[Course]              - список курсов
    """
    valid_tags = [tag for tag in tags if tag]

    if valid_tags:
        return courses.filter(tags__in=valid_tags).distinct()

    return courses


def sort_courses(sort: str, courses: list[Course]) -> list[Course]:
    """
        Сортировка статей

        :param  sort: str                - строка для сортировки
        :param  courses: [Course]        - список курсов
        :return [Course]                 - список курсов
    """

    if sort == 'Newest':
        courses = courses.order_by('-created')
    elif sort == 'Oldest':
        courses = courses.order_by('created')
    elif sort == 'Popular':
        courses = courses.annotate(likes_count=Count('reactions')).order_by('-likes_count')
    elif sort == 'Unpopular':
        courses = courses.annotate(likes_count=Count('reactions')).order_by('likes_count')
    return courses


def add_remove_like_to_course(course: Course, user: User) -> str:
    """
        Добавление и удаление лайка к курсу

        :param course: Course - Курс
        :param user: User     - Пользователь
        :return str           - Сообщение
    """
    if user in course.likes.all():
        course.likes.remove(user)
        return 'User\'s like removed successfully!'
    course.likes.add(user)
    return 'The course liked successfully!'


def add_remove_registration_to_course(course: Course, user: User) -> str:
    """
        Регистрация и удаление пользователя с курса

        :param course: Course - Курс
        :param user: User - Пользователь
        :return str - Сообщение о результате операции
    """
    if user in course.users_who_registered.all():
        course.users_who_registered.remove(user)
        return 'Course was removed from user profile successfully'
    else:
        course.users_who_registered.add(user)
        return 'Course was added to user profile successfully'


def is_user_registered_to_course(course: Course, user: User) -> bool:
    """
         Проверка завершения задания пользователем

         :param course: Course - Курс
         :param user: User - Пользователь
         :return bool - Статус
    """
    return user in course.users_who_registered.all()


def delete_course(course: Course):
    """
        Удаление курса

        :param course: Course - Курс
    """
    course.delete()
