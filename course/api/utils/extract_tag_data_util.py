from typing import List, Dict, Any

from course.models import Tag


def extract_tag_data_util(tags: [Tag]) -> list[dict[str, Any]]:
    """
         Генерация списка с словарями данных тэгов

         :param tags[Tag] - список тэгов
         :return: list[dict[str, Any]]
    """
    return [{
        'id': tag.id,
        'name': tag.name,
    } for tag in tags]
