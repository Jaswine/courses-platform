from pytest import mark

from apps.article.api.services.article_reaction_service import get_first_existing_reactions, toggle_reaction


@mark.django_db
def test_get_first_existing_reactions(published_article, user, user_reaction):
    """
        Взятие первой существующей реакции
    """
    published_article.reactions.add(user_reaction)

    reaction = get_first_existing_reactions(published_article, user)

    assert reaction is not None
    assert reaction == user_reaction


@mark.django_db
def test_toggle_reaction_reaction_is_not_exist(published_article, user, user_reaction):
    """
        Создание первой реакции
    """
    published_article.reactions.remove(user_reaction)
    message = toggle_reaction(published_article, user, "Like")

    assert message is not None
    assert message == 'Reaction added!'
    assert published_article.reactions.count() == 1
    assert published_article.reactions.filter(reaction_type='Like').exists()


@mark.django_db
def test_toggle_reaction_the_same_reaction_is_exist(published_article, user, user_reaction):
    """
        Удаление реакции
    """
    message = toggle_reaction(published_article, user, "Like")

    assert message is not None
    assert message == 'Reaction removed!'
    assert published_article.reactions.count() == 0
    assert user_reaction not in published_article.reactions.all()


@mark.django_db
def test_toggle_reaction_another_reaction_is_exist(published_article, user, user_reaction):
    """
        Изменение реакции
    """
    published_article.reactions.add(user_reaction)

    message = toggle_reaction(published_article, user, "Unicorn")

    assert message is not None
    assert message == 'Reaction updated!'
    assert published_article.reactions.count() == 1
    assert user_reaction.reaction_type != published_article.reactions.first().reaction_type
