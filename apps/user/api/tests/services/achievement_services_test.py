from pytest import mark

from apps.user.api.services.achievement_service import find_all_achievements, get_achievement_by_id


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


@mark.django_db
def test_get_achievement_by_id(achievement_list):
    """test_get_achievement_by_id
        Взятие достижения по его идентификатору
    """
    element = achievement_list[0]
    achievement = get_achievement_by_id(element.id)

    assert achievement is not None
    assert achievement.id == element.id
    assert achievement.title == element.title