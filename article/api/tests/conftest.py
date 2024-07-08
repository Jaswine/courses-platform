from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from pytest import fixture

from article.models import Article, ArticleComment
from course.models import Tag
from user.models import Reaction


@fixture
def tag1(db):
    return Tag.objects.create(name='Tag1')


@fixture
def tag2(db):
    return Tag.objects.create(name='Tag2')


@fixture
def user(db):
    return User.objects.create(username='user',
                               email='user@example.com',
                               password=make_password('password'))


@fixture
def unpublished_article(db, user, tag2):
    unpublished_article = Article.objects.create(title='Unpublished Article',
                                                 user=user,
                                                 content='This is a unpublished article.',
                                                 is_published=False,
                                                 created=datetime.now() - timedelta(days=2))
    unpublished_article.tags.add(tag2)
    return unpublished_article


@fixture
def published_article(db, user, tag1, user_reaction):
    published_article = Article.objects.create(title='Published Article',
                                               user=user,
                                               content='This is a published article.',
                                               is_published=True,
                                               created=datetime.now() - timedelta(days=1))
    published_article.tags.add(tag1)
    published_article.reactions.add(user_reaction)
    return published_article


@fixture
def article_list():
    return Article.objects.all()


@fixture
def article_comment(db, published_article, user):
    return ArticleComment.objects.create(article=published_article,
                                         user=user,
                                         message='Test message')


@fixture
def user_reaction(db, user):
    return Reaction.objects.create(user=user,
                                   reaction_type='Like')

