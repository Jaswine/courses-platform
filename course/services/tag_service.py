from course.models import Tag


def get_all_tags() -> list[Tag]:
    """
        Взятие всех тэгов

        :return: list[Tag] - список тэгов
    """
    return Tag.objects.all()
