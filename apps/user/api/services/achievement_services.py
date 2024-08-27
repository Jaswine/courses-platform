from typing import List

from apps.user.models import Achievement


def find_all_achievements() -> List[Achievement]:
    """
        Вывод всех пользователей

        :return List[Achievement] - Список достижений
    """
    return Achievement.objects.all()