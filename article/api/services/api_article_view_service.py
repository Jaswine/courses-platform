from django.contrib.auth.models import User
from article.models import Article


def add_view_to_article(article: Article, user: User) -> str:
    """
        Добавление просмотра к статье

        :param: article: Article    - Статья
        :param: user: User          - Пользователь
        :return: str                - Сообщение
    """
    if user not in article.views.all():
        article.views.add(user)
        return 'View added successfully!'
    return 'View already added!'
