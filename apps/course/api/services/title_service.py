from apps.course.models import TitleOrder, Title, Course


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


def update_course_title_name(course_title: Title, title: str) -> str | None:
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
    except Exception as e:
        print(e)
        return None


def update_course_title_public(course_title: Title, status: bool) -> str | None:
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
    except Exception as e:
        print(e)
        return None


def delete_course_title(course_title: Title):
    """
        Удаление темы курса

        :param course_title: Title - Тема курса
    """
    course_title.delete()


def get_title_order_by_course_id_and_title_id(course_id: int, course_title_id: int) -> TitleOrder:
    """
        Взятие места темы в списке тем курса

        :param course_id: int - Идентификатор курса
        :param course_title_id: int - Идентификатор темы курса
        :return TitleOrder - Место темы
    """
    try:
        return TitleOrder.objects.get(course_id=course_id, title_id=course_title_id)
    except TitleOrder.DoesNotExist:
        return None


def update_titles_places(course: Course, title1: Title, title2: Title) -> bool:
    """
        Смена тем местами

        :param course: Course - Курс
        :param title1: Title - Тема курса 1
        :param title2: Title - Тема курса 2
        :return bool - Статус
    """
    try:
        # Поиск объектов TitleOrder
        title_order1 = get_title_order_by_course_id_and_title_id(course.id, title1.id)
        title_order2 = get_title_order_by_course_id_and_title_id(course.id, title2.id)

        # Изменение их местами, изменив поле `order`
        title_order1.order, title_order2.order = title_order2.order, title_order1.order

        # Сохранение изменений
        title_order1.save()
        title_order2.save()

        return True
    except Exception as e:
        print(e)
        return False
