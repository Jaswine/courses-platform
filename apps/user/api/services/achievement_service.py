from typing import List

from apps.user.models import Achievement


def find_all_achievements() -> List[Achievement]:
    """
        Вывод всех пользователей

        :return List[Achievement] - Список достижений
    """
    return Achievement.objects.all()


def get_achievement_by_id(achievement_id: int) -> Achievement | None:
    """
        Взятие достижения по его идентификатору

        :param achievement_id: int - Идентификатор достижения
        :return Achievement -  Достижение
    """
    try:
        return Achievement.objects.get(id=achievement_id)
    except Achievement.DoesNotExist:
        return None


def delete_achievement(achievement: Achievement):
    """
        Удаление достижения по его идентификатору

        :param achievement: Achievement -  Достижение
    """
    achievement.delete()
