from pytest import mark

from apps.article.api.services.article_view_service import add_view_to_article


@mark.django_db
def test_add_view_to_article_user_is_not_in_article_views(published_article, user):
    """
        Добавление просмотра, если пользователь еще не смотрел
    """
    message = add_view_to_article(published_article, user)

    assert message is not None
    assert message == 'View added successfully!'
    assert published_article.views.count() == 1
    assert published_article.views.first() == user


@mark.django_db
def test_add_view_to_article_user_is_in_article_views(published_article, user):
    """
        Сообщение, что выводится, если просмотр существует
    """
    published_article.views.add(user)
    message = add_view_to_article(published_article, user)

    assert message is not None
    assert message == 'View already added!'
    assert published_article.views.count() == 1
    assert published_article.views.first() == user

