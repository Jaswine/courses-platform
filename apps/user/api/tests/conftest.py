from django.contrib.auth.hashers import make_password
from pytest import fixture

from apps.user.models import User, Achievement


@fixture
def achievement_list(db):
    achievements = []
    for i in range(6):
        achievement = Achievement.objects.create(
            title=f'Title{i}',
            description=f'Description{i}',
            type='courses' if i % 2 == 0 else 'tasks',
            target_value=5 * i
        )
        achievements.append(achievement)
    return achievements


@fixture
def user_list(db):
    users = []
    for i in range(6):
        user = User.objects.create(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password=make_password('password'),
            first_name=f'First{i}',
            last_name=f'Last{i}',
            is_active=True if i % 2 == 0 else False,
            is_blocked=True if i % 2 == 0 else False,
            is_superuser=True if i % 2 == 0 else False,
            scores=10 * i,
        )
        users.append(user)
    return users
