from apps.user.models import User
from rest_framework_simplejwt.tokens import RefreshToken, Token


def generate_tokens(user: User) -> (str, str):
    """
        Генерация access и refresh токенов для пользователя

        :param user: User - Пользователь
        :return Token токены
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)