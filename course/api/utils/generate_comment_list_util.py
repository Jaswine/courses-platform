from typing import List, Dict, Any

from django.contrib.auth.models import User

from article.models import ArticleComment
from course.models import TaskComment


def generate_comment_list_util(comments: [TaskComment | ArticleComment], user: User, depth=0) -> list[
    dict[str, dict[str, Any | None] | dict[str, bool | Any] | Any]]:
    """
        Генерация списка с словарями данных комментариев

        :param comments: TaskComment | ArticleComment       - Список комментариев
        :param : user: User                                 - Пользователь
        :return [dict[str, bool | None | list[dict[str, Any]] | Any]] - Список
            с словарями комментариев
    """
    return generate_comment_util(comments, user, depth)


def generate_comment_util(comments, user, depth):
    comment_list = []
    for comment in comments:
        if comment.is_public:
            data = dict()
            data['id'] = comment.id
            data['user'] = {
                'id': comment.user.id,
                'username': comment.user.username,
                'ava': comment.user.profile.image.url if comment.user.profile.image else None,
            }
            data['likes'] = {
                'count': comment.likes.count(),
                'my': True if user in comment.likes.all() else False,
            }

            data['message'] = comment.text
            data['is_liked'] = True if user in comment.likes.all() else False

            data['created'] = comment.created.strftime("%H:%M %d.%m.%Y")
            data['updated'] = comment.updated.strftime("%H:%M %d.%m.%Y")
            data['depth'] = depth

            if comment.task_comment_children.count() > 0:
                data['children'] = generate_comment_list_util(comment.task_comment_children.all(), user, depth+1)

            comment_list.append(data)

    return comment_list
