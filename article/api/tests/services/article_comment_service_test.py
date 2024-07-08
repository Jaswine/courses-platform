from django.contrib.auth.models import User
from pytest import fixture
from pytest import mark

from article.api.services.api_article_comment_service import filter_comments_by_article
from article.api.services.api_article_view_service import add_view_to_article
from article.models import Article, ArticleComment


@fixture
def user(db):
    return User.objects.create(username='user',
                               email='email@example.com',
                               password='password')


@fixture
def article(db, user):
    return Article.objects.create(title='Published Article',
                                  user=user,
                                  content='This is a published article.',
                                  is_published=True)


@fixture
def article_comment(db, article, user):
    return ArticleComment.objects.create(article=article,
                                         user=user,
                                         message='Test message')


@mark.django_db
def test_filter_comments_by_article(article, article_comment):
    """
        Взятие комментариев для статьи
    """
    article_comments = filter_comments_by_article(article)

    assert len(article_comments) == 1
    assert article_comments[0] == article_comment

