from django.contrib.auth.models import User
from pytest import fixture
from pytest import mark

from article.api.services.api_article_view_service import add_view_to_article
from article.models import Article


@fixture
def user(db):
    return User.objects.create(username='user',
                               email='email@example.com',
                               password='password')


@fixture
def article(db, user):
    return Article.objects.create(title='Published Article',
                                  user=user,
                                  content='This is a published article.')


@mark.django_db
def test_add_view_to_article_user_is_not_in_article_views(article, user):
    """
        Добавление просмотра, если пользователь еще не смотрел
    """
    message = add_view_to_article(article, user)

    assert message is not None
    assert message == 'View added successfully!'
    assert article.views.count() == 1
    assert article.views.first() == user


@mark.django_db
def test_add_view_to_article_user_is_in_article_views(article, user):
    """
        Сообщение, что выводится, если просмотр существует
    """
    article.views.add(user)
    message = add_view_to_article(article, user)

    assert message is not None
    assert message == 'View already added!'
    assert article.views.count() == 1
    assert article.views.first() == user

