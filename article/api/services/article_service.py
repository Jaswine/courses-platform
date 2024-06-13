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
        articles.sort(key=lambda article: article.created_at, reverse=True)
    elif sort == 'Oldest':
        articles.sort(key=lambda article: article.created_at, reverse=False)
    elif sort == 'Popular':
        articles.sort(key=lambda article: article.likes.count(), reverse=True)
    elif sort == 'Unpopular':
        articles.sort(key=lambda article: article.likes.count(), reverse=False)

    return articles
