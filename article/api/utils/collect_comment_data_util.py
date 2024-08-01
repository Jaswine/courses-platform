from typing import List, Dict

from article.models import ArticleComment


def collect_comment_data_util(comments: list[ArticleComment]) -> (
        list)[dict[str, str | int]]:
    """
        Генерация списка с словарями статей

        :param comments: list[ArticleComment]   - Список комментариев
        :return  list[dict[str, str | int]]     - Список с словарями данных коммент
    """
    return [{
        'id': comment.id,
        'message': comment.message,
    } for comment in comments]
