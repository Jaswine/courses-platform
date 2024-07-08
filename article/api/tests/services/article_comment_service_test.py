from pytest import mark
from article.api.services.api_article_comment_service import filter_comments_by_article


@mark.django_db
def test_filter_comments_by_article(published_article, article_comment):
    """
        Взятие комментариев для статьи
    """
    article_comments = filter_comments_by_article(published_article)

    assert len(article_comments) == 1
    assert article_comments[0] == article_comment

