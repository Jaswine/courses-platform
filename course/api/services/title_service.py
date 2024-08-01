from course.models import TitleOrder, Title, Course


def get_course_titles_by_course_id(course_id: int) -> list[TitleOrder]:
    """
        Взятие тем курсов по id курса

        :param course_id: int      - id курса
        :return list[TitleOrder]   - список тем курсов
    """
    title_orders = TitleOrder.objects.filter(course_id=course_id).order_by('order')
    return [title_order.title for title_order in title_orders]


def get_course_title_by_id(id: int) -> Title | None:
    """
        Взятие темы по идентификатору

        :param id: int - Идентификатор темы
        :return Title | None - Тема
    """
    try:
        return Title.objects.get(id=id)
    except Title.DoesNotExist:
        return None


def filter_course_titles_by_id(course_id: int) -> list[Title]:
    """
        Фильтрация тем курсов

        :param course_id: int - Идентификатор курса
        :return list[Title] - Список тем курсов
    """
    title_orders = TitleOrder.objects.filter(course_id=course_id).order_by('order')
    return [title_order.title for title_order in title_orders]


def create_course_title_order(course: Course, title: Title) -> TitleOrder | None:
    """
        Создание места для темы

        :param course: Course - Курс
        :param title: Title - Тема
        :return TitleOrder | None
    """
    order = course.course_titles.count() + 1
    return TitleOrder.objects.create(course=course, title=title, order=order)


def create_course_title(course: Course, title: str) -> Title | None:
    """
        Создание темы для курса

        :param course: Course - Курс
        :param title: str - Название темы
        :return Title | None
    """
    title = Title.objects.create(title=title)

    if create_course_title_order(course, title):
        return title
    return None


def update_course_title_name(course_title: Title, title: str) -> str:
    """
        Обновление названия темы курса

        :param course_title: Title - Темы курса
        :param title: str - Название темы
        :return bool
    """
    try:
        course_title.title = title
        course_title.save()
        return 'Title updated successfully!'
    except:
        return False


def update_course_title_public(course_title: Title, status: bool) -> str:
    """
        Обновление публичности темы курса

        :param course_title: Title - Темы курса
        :param status: str - мм
        :return bool
    """
    try:
        course_title.public = status
        course_title.save()
        return 'Title updated successfully!'
    except:
        return False


def delete_course_title(course_title: Title):
    """
        Удаление темы курса

        :param course_title: Title - Тема курса
    """
    course_title.delete()
