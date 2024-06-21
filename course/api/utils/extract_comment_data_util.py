from typing import List, Dict, Any

from django.contrib.auth.models import User

from article.models import ArticleComment
from course.models import TaskComment


def generate_comment_list_util(comments: [TaskComment | ArticleComment], user: User) -> list[
    dict[str, dict[str, Any | None] | dict[str, bool | Any] | Any]]:
    """
        Генерация списка с словарями данных комментариев

        :param comments: TaskComment | ArticleComment       - Список комментариев
        :param : user: User                                 - Пользователь
        :return [dict[str, bool | None | list[dict[str, Any]] | Any]] - Список
            с словарями комментариев
    """
    return [{
        'id': comment.id,
        'user': {
            'username': comment.user.username,
            'ava': comment.user.profile.image.url if comment.user.profile.image else None,
        },
        'likes': {
            'count': comment.likes.count(),
            'my': True if user in comment.likes.all() else False,
        },
        'message': comment.text,
        'created': comment.created.strftime("%H:%M %d.%m.%Y"),
        'updated': comment.updated.strftime("%H:%M %d.%m.%Y"),
    } for comment in comments]
