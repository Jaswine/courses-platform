from pytest import mark
from pytest import fixture

from apps.article.api.utils.collect_article_data_util import collect_article_data_utils
from datetime import datetime


@fixture
def article_list(db, published_article):
    return [published_article]


@mark.django_db
def test_collect_article_data_utils(article_list):
    """
        Генерация списка с словарями статей
    """
    expected_result = [{
        'id': 1,
        'title': 'Published Article',
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
