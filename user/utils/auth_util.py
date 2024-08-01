from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

from user.services.user_service import get_user_by_email


def authenticate(email: str, password: str) -> User | None:
    """
        Аутентификация пользователя

       :param email: str     - электронная почта
       :param password: str  - пароль
       :return User or None  - Пользователь
    """
    user = get_user_by_email(email)

    if user and check_password(password, user.password):
        return user
    return None

