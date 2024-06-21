from course.models import Tag


def get_all_tags() -> [Tag]:
    """
        Вывод списка тэгов

        :return [Tag]  - список тэгов
    """
    return Tag.objects.all()


def filter_tags_by_name(tags: [Tag], name: str) -> [Tag]:
    """
        Фильтрация тэгов

        :param tags: [Tag]   - список тэгов
        :param name: str     - название тэга
        :return [Tag]        - список тэгов
    """
    return tags.filter(name__icontains=name)


def create_new_tag(name: str) -> Tag | None:
    """
        Создание нового тега

        :param name: str    - Название
        :return Tag         - Тэг
    """
    return Tag.objects.create(name=name)


def get_tag_by_id(tag_id: int) -> Tag | None:
    """
        Взятие тэга по id

        :param tag_id: int   - id тэга
        :return Tag           - тэш
    """
    return Tag.objects.get(id=tag_id)


def update_tag(tag: Tag, name: str) -> None:
    """
        Обновление тэга

        :param tag: Tag - тэг
        :param name: str - название тэга
    """
    tag.name = name
    tag.save()


def delete_tag(tag: Tag) -> None:
    """
        Удаление тэга

        :param tag: Tag - тэг
    """
    tag.delete()
