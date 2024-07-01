from django.db.models import Count

from article.models import Article
from course.models import Tag


def get_all_articles() -> list[Article]:
    """
        Взятие всех статей

        :return [Article]
    """
    return Article.objects.all()


def filter_articles(is_superuser: bool, q: str, tags: [Tag]) -> list[Article]:
    """
        Фильтрация статей

        :param  is_superuser: bool  - пользователь
        :param  q: str              - строка для поиска
        :param  tags: [Tag]         - строка для фильтрации по тегам
        :return [Article]
    """
    articles = Article.objects.filter(title__icontains=q)

    if not is_superuser:
        articles.filter(is_published=True)

    valid_tags = [tag for tag in tags if tag]

    if valid_tags:
        articles = articles.filter(tags__in=tags).distinct()

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
