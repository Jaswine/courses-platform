from course.models import Tag


def get_all_tags() -> list[Tag]:
    """
        Взятие всех тэгов

        :return list[Tag] - список тэгов
    """
    return Tag.objects.all()


def find_tags_by_name(name: str) -> list[Tag]:
    """
        Фильтрация тэгов по именам

        :param name: str           - имя тэга
        :return list[Tag]          - список тэгов
    """
    return Tag.objects.filter(name__icontains=name)


def create_tag(name: str) -> Tag | None:
    """
        Создание тэга

        :param name: str    - название тэга
        :return Tag | None  - тэг
    """
    return Tag.objects.create(name=name)


def get_tag_by_id(id: int) -> Tag | None:
    """
        Взятие тэга по идентификатору

        :param id: int      - Идентификатор тэга
        :return Tag | None   - Тэг
    """
    try:
        return Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        return None


def update_tag_name(name: str, tag: Tag) -> Tag:
    """
        Обновление тэга

        :param name: str    - Имя тэга
        :param tag: Tag     - тэг
        :return Tag         - тэг
    """
    tag.name = name
    tag.save()

    return tag


def delete_tag(tag: Tag):
    """
        Удаление тэга

        :param tag: Tag  - тэг
    """
    tag.delete()
