from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from pytest import fixture

from apps.user.models import Profile


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
            is_superuser=True if i % 2 == 0 else False,
        )
        Profile.objects.create(user=user, scores=i*10)
        users.append(user)
    return users

