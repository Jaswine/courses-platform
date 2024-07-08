from pytest import mark
from pytest import fixture

from article.api.utils.collect_article_data_util import collect_article_data_utils
from article.models import Article
from course.models import Tag
from user.models import Reaction
from django.contrib.auth.models import User

from datetime import datetime, timedelta


@fixture
def tag1(db):
    return Tag.objects.create(name='Tag1')


@fixture
def user(db):
    return User.objects.create(username='user',
                               email='user@example.com',
                               password='')


@fixture
def user_reaction(db, user):
    return Reaction.objects.create(user=user,
                                   reaction_type='Like')


@fixture
def article_1(db, user, tag1, user_reaction):
    article = Article.objects.create(title='Article 1',
                                     user=user,
                                     content='This is a published article.')
    article.tags.add(tag1)
    article.reactions.add(user_reaction)
    return article


@fixture
def article_list(db, article_1):
    return [article_1]


@mark.django_db
def test_collect_article_data_utils(article_list):
    """
        Генерация списка с словарями статей
    """
    expected_result = [{
        'id': 1,
        'title': 'Article 1',
        'image': None,
        'tags': [{
            'id': 1,
            'name': 'Tag1',
        }],
        'user': 'user',
        'likes_count': 1,
        'comments_count': 0,
        'created': datetime.now().strftime('%d.%m.%Y'),
        'updated': datetime.now().strftime('%d.%m.%Y'),
    }]

    result = collect_article_data_utils(article_list)

    assert type(result) is list
    assert expected_result == result
