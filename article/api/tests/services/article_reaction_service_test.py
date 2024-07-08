from django.contrib.auth.models import User
from pytest import fixture
from pytest import mark

from article.api.services.api_article_reaction_service import get_first_existing_reactions, toggle_reaction
from article.models import Article
from user.models import Reaction


@fixture
def user(db):
    return User.objects.create(username='user',
                               email='email@example.com',
                               password='password')


@fixture
def reaction(db, user):
    return Reaction.objects.create(user=user,
                                   reaction_type='Like')


@fixture
def article(db, user, reaction):
    return Article.objects.create(title='Published Article',
                                  user=user,
                                  content='This is a published article.')


@mark.django_db
def test_get_first_existing_reactions(article, user, reaction):
    """
        Взятие первой существующей реакции
    """
    article.reactions.add(reaction)

    reaction = get_first_existing_reactions(article, user)

    assert reaction is not None
    assert reaction == reaction


@mark.django_db
def test_toggle_reaction_reaction_is_not_exist(article, user):
    """
        Создание первой реакции
    """
    message = toggle_reaction(article, user, "Like")

    assert message is not None
    assert message == 'Reaction added!'
    assert article.reactions.count() == 1
    assert article.reactions.filter(reaction_type='Like').exists()


@mark.django_db
def test_toggle_reaction_the_same_reaction_is_exist(article, user, reaction):
    """
        Удаление реакции
    """
    article.reactions.add(reaction)

    message = toggle_reaction(article, user, "Like")

    assert message is not None
    assert message == 'Reaction removed!'
    assert article.reactions.count() == 0
    assert reaction not in article.reactions.all()


@mark.django_db
def test_toggle_reaction_another_reaction_is_exist(article, user, reaction):
    """
        Изменение реакции
    """
    article.reactions.add(reaction)

    message = toggle_reaction(article, user, "Unicorn")

    assert message is not None
    assert message == 'Reaction updated!'
    assert article.reactions.count() == 1
    assert reaction.reaction_type != article.reactions.first().reaction_type
