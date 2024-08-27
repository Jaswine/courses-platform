from pytest import mark

from apps.user.api.services.achievement_services import find_all_achievements


@mark.django_db
def test_find_all_achievements(achievement_list):
    """
        Взятие всех достижений
    """
    achievements = find_all_achievements()

    assert achievements is not None
    assert len(achievement_list) == len(achievements)
    assert achievements[0] in achievement_list
    assert achievements[1] in achievement_list