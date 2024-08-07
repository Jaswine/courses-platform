from typing import Any

from apps.article.models import Article, ArticleComment


def collect_article_data_utils(articles: list[Article]) -> list[
        dict[str, None | str | int | list[dict[str, Any]] | Any]]:
    """
        Генерация списка с словарями статей

        :param   articles: list[Article] - список статей
        :return  list[dict[str, None | str | int | list[dict[str, Any]] | Any]] - Список
            с словарями данных статей
    """
    return [{
        'id': article.id,
        'title': article.title,
        'image': article.image.url if article.image else None,
        'tags': [{
            'id': tag.id,
            'name': tag.name,
        } for tag in article.tags.all()],
        'user': article.user.username,
        'likes_count': article.reactions.count(),
        'comments_count': ArticleComment.objects.filter(article=article).count(),
        'created': article.created.strftime('%d.%m.%Y'),
        'updated': article.updated.strftime('%d.%m.%Y'),
    } for article in articles]
