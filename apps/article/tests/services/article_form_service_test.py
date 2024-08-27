from pytest import fixture, mark

from apps.article.forms import ArticleForm
from apps.article.models import Article
from apps.article.services.article_form_service import create_article, update_article, delete_article
from apps.course.models import Tag
from apps.user.models import User


@fixture
def user(db):
    return User.objects.create(username='user',
                email='user@example.com',
                password='password')


@fixture
def tag(db):
    return Tag(name='tag')


@fixture
def article(db, user):
    return Article.objects.create(title='Article',
                                  user=user,
                                  content='Some content')


@fixture
def valid_article_form(tag):
    form_data = {
        'title': 'Test Article',
        'image': None,
        'content': 'This is a test article content.',
        'tags': [],
        'is_published': False,
    }
    form = ArticleForm(data=form_data)
    return form


@fixture
def valid_update_article_form(tag, article):
    form_data = {
        'title': 'Updated Test Article',
        'image': None,
        'content': 'This is a test article content.',
        'tags': [],
        'is_published': False,
    }
    form = ArticleForm(data=form_data, instance=article)
    return form


def test_create_article_valid_form(valid_article_form, user):
    """
        Сохранение статьи, правильные данные
    """
    article = create_article(valid_article_form, user)

    assert article is not None
    assert article.title == 'Test Article'
    assert article.content == 'This is a test article content.'
    assert article.user == user


def test_create_article_invalid_form():
    """
        Сохранение статьи, не правильные данные
    """
    form = ArticleForm(data={})
    assert not form.is_valid()

    article = create_article(form, User())
    assert article is None


def test_update_article_valid_form(valid_update_article_form):
    """
        Обновление статьи, правильные данные
    """
    article = update_article(valid_update_article_form)

    assert article is not None
    assert article.title == 'Updated Test Article'


def test_update_article_invalid_form():
    """
        Обновление статьи, не правильные данные
    """
    form = ArticleForm(data={})
    assert not form.is_valid()

    article = update_article(form)
    assert article is None


def test_delete_article(article):
    """
        Удаление статьи
    """
    delete_article(article)

    assert Article.objects.count() == 0
