
from apps.article.models import Article
from apps.user.models import Reaction, User
from apps.user.services.reaction_service import create_reaction


def get_first_existing_reactions(article: Article, user: User) -> Reaction:
    """
        Взятие первой существующей реакции

        :param article: Article    - Статья
        :param user: User          - Пользователь
        :return  Reaction           - Список реакций
    """
    return article.reactions.filter(user=user).first()


def toggle_reaction(article: Article, user: User, reaction_type: str) -> str:
    """
        Добавление / изменение / удаление реакции

        :param article: Article    - Статья
        :param user: User          - Пользователь
        :param reaction_type: str  - Наименование реакции
        :return str                - Сообщение
    """
    existing_reaction = get_first_existing_reactions(article, user)
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            article.reactions.remove(existing_reaction)
            existing_reaction.delete()
            return 'Reaction removed!'
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            return 'Reaction updated!'
    else:
        new_reaction = create_reaction(user, reaction_type)
        article.reactions.add(new_reaction)
        return 'Reaction added!'
