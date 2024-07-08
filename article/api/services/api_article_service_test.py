from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q

from article.models import Article
from course.models import Tag


def get_all_articles() -> list[Article]:
    """
        Взятие всех статей

        :return [Article]
    """
    return Article.objects.all()


def find_articles_by_user_status(user_status: bool) -> list[Article]:
    """
        Взятие статей взависимости от типа пользователя

        :return [Article] - список статей
    """
    return Article.objects.all() if user_status else Article.objects.filter(is_published=True)


def search_articles_by_title(q: str, articles: list[Article]) -> list[Article]:
    """
        Поиск статей

        :param  q: str              - строка для поиска
        :param  articles: list[Article]   - список статей
        :return list[Article]       - список статей
    """
    return articles.filter(Q(title__icontains=q))


def filter_articles_by_tags(tags: [Tag], articles: list[Article]) -> list[Article]:
    """
        Фильтрация статей

        :param  tags: [Tag]               - строка для фильтрации по тегам
        :param  articles: list[Article]   - список статей
        :return [Article]                 - список статей
    """
    valid_tags = [tag for tag in tags if tag]

    if valid_tags:
        return articles.filter(tags__in=valid_tags).distinct()
    return articles


def sort_articles(sort: str, articles: list[Article]) -> list[Article]:
    """
        Сортировка статей

        :param  sort: str                - строка для сортировки
        :param  articles: [Article]      - список статей
        :return [Article]
    """

    if sort == 'Newest':
        articles = articles.order_by('-created')
    elif sort == 'Oldest':
        articles = articles.order_by('created')
    elif sort == 'Popular':
        articles = articles.annotate(likes_count=Count('reactions')).order_by('-likes_count')
    elif sort == 'Unpopular':
        articles = articles.annotate(likes_count=Count('reactions')).order_by('likes_count')

    return articles
