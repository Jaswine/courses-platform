from article.models import ArticleComment, Article


def filter_comments_by_article(article: Article) -> list[ArticleComment]:
    """
        Взятие комментариев для статьи

        :param: article: Article       - Статья
        :return: list[ArticleComment]  - Список комментариев
    """
    return ArticleComment.objects.filter(article=article)
