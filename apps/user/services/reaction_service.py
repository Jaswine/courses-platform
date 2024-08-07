from django.contrib.auth.models import User

from apps.user.models import Reaction


def create_reaction(user: User, reaction_type: str) -> Reaction:
    """
        Создание новой реакции

        :param user: User              - Пользователь
        :param reaction_type: str      - Наименование реакции
        :return Reaction               - Реакция
    """
    return Reaction.objects.create(user=user,
                                   reaction_type=reaction_type)
