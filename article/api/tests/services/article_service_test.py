from pytest import fixture
from pytest import mark

from article.api.services.api_article_service_test import *

from user.models import Reaction
from article.models import Article
from django.contrib.auth.models import User

from datetime import datetime, timedelta


@fixture
def tag1(db):
    return Tag.objects.create(name='Tag1')


@fixture
def tag2(db):
    return Tag.objects.create(name='Tag2')


@fixture
def user1(db):
    return User.objects.create(username='user1',
                               email='user1@example.com',
                               password='')


@fixture
def user_reaction(db, user1):
    return Reaction.objects.create(user=user1,
                                   reaction_type='Like')


@fixture
def published_article(db, user1, tag1, user_reaction):
    article = Article.objects.create(title='Published Article',
                                     user=user1,
                                     content='This is a published article.',
                                     is_published=True,
                                     created=datetime.now() - timedelta(days=1))
    article.tags.add(tag1)
    article.reactions.add(user_reaction)
    return article


@fixture
def unpublished_article(db, user1, tag2):
    article = Article.objects.create(title='Unpublished Article',
                                     user=user1,
                                     content='This is a unpublished article.',
                                     is_published=False,
                                     created=datetime.now() - timedelta(days=2))
    article.tags.add(tag2)
    return article


@fixture
def article_list():
    return Article.objects.all()


@mark.django_db
def test_get_all_articles(published_article,
                          unpublished_article):
    """
        Успешное взятие всех статей
    """
    articles = get_all_articles()

    assert len(articles) == 2
    assert published_article in articles
    assert unpublished_article in articles


@mark.django_db
def test_find_articles_by_user_status_when_user_is_superuser(published_article,
                                                             unpublished_article):
    """
        Поиск статей с фильтрацией,
            если пользователь имеет статус супер пользователя
    """
    articles = find_articles_by_user_status(True)

    assert len(articles) == 2
    assert published_article in articles
    assert unpublished_article in articles


@mark.django_db
def test_find_articles_by_user_status_when_user_is_not_superuser(published_article,
                                                                 unpublished_article):
    """
       Поиск статей с фильтрацией,
           если пользователь не имеет статус супер пользователя
    """
    articles = find_articles_by_user_status(False)

    assert len(articles) == 1
    assert published_article in articles
    assert unpublished_article not in articles


@mark.django_db
def test_search_articles_by_title(article_list,
                                  published_article,
                                  unpublished_article):
    """
        Поиск статей по названия
    """
    articles = search_articles_by_title(unpublished_article.title,
                                        article_list)

    assert len(articles) == 1
    assert unpublished_article in articles
    assert published_article not in articles


@mark.django_db
def test_filter_articles_by_tags(article_list,
                                 published_article,
                                 unpublished_article,
                                 tag1):
    """
        Фильтрация статей по тегам
    """
    articles = filter_articles_by_tags([tag1.id],
                                       article_list)

    assert len(articles) == 1
    assert published_article in articles
    assert unpublished_article not in articles


@mark.django_db
def test_sort_articles_by_nothing(article_list, published_article, unpublished_article):
    """
        Сортировка статей с передачей пустого, неподходящего параметра
    """
    articles = sort_articles('', article_list)

    assert len(articles) == 2
    assert published_article in articles and unpublished_article in articles


@mark.django_db
def test_sort_articles_by_newest(article_list, published_article, unpublished_article):
    """
        Сортировка статей по дате, от новых к старым
    """
    articles = sort_articles('Newest', article_list)

    assert len(articles) == 2
    assert articles[0] == unpublished_article
    assert articles[1] == published_article


@mark.django_db
def test_sort_articles_by_oldest(article_list, published_article, unpublished_article):
    """
        Сортировка статей по дате, от старым к новым
    """
    articles = sort_articles('Oldest', article_list)

    assert len(articles) == 2
    assert articles[0] == published_article
    assert articles[1] == unpublished_article


@mark.django_db
def test_sort_articles_by_popular(article_list, published_article, unpublished_article):
    """
        Сортировка статей по дате, от самых популярных к не популярным
    """
    articles = sort_articles('Popular', article_list)

    assert len(articles) == 2
    assert articles[0] == published_article
    assert articles[1] == unpublished_article


@mark.django_db
def test_sort_articles_by_unpopular(article_list, published_article, unpublished_article):
    """
        Сортировка статей по дате, от самых не популярных к популярным
    """
    articles = sort_articles('Unpopular', article_list)

    assert len(articles) == 2
    assert articles[0] == unpublished_article
    assert articles[1] == published_article
