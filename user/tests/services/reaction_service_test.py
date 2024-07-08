from pytest import mark
from user.services.reaction_service import create_reaction


@mark.django_db
def test_create_reaction(user):
    """
        Создание реакции
    """
    reaction = create_reaction(user, 'Like')

    assert reaction is not None
    assert reaction.user == user
    assert reaction.reaction_type == 'Like'

