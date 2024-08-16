from unittest.mock import patch
from apps.user.utils.auth_util import authenticate


@patch('user.services.user_service.get_user_by_email')
def test_authenticate_success(get_user_by_email,
                              user):
    """
        Успешная аутентификация пользователя
    """
    get_user_by_email.return_value = user

    current_user = authenticate('user@example.com', 'password')

    assert current_user is not None
    assert current_user.email == user.email


@patch('user.services.user_service.get_user_by_email')
def test_authenticate_email_not_found(get_user_by_email,
                                      user):
    """
        Аутентификация пользователя, пользователь не найден
    """
    get_user_by_email.return_value = None

    current_user = authenticate('user1@example.com', 'password')

    assert current_user is None


@patch('user.services.user_service.get_user_by_email')
def test_authenticate_incorrect_password(get_user_by_email,
                                         user):
    """
        Аутентификация пользователя, неправильный пароль
    """
    get_user_by_email.return_value = user

    current_user = authenticate('user@example.com', 'password1')

    assert current_user is None
