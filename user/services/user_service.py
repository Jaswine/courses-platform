from django.contrib.auth.models import User

from user.forms import CreateUserForm, UpdateUserForm, UpdateProfileForm
from user.models import Profile


def get_user_by_email(email: str) -> User | None:
    """
        Взятие пользователя по электронной почте

        :param: email: str    - Электронная почта
        :return: User | None   - Пользователь или None
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_user_by_username(username: str) -> User | None:
    """
        Взятие пользователя по имени пользователя

        :param: username: str    - Имя пользователя
        :return: User | None   - Пользователь или None
    """
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def create_user_and_profile_by_form(form: CreateUserForm) -> User | None:
    """
        Создание пользователя с его профиля, используя форму

        :param: form: CreateUserForm  - Форма для создания пользователя
        :return: User     - Пользователь
    """
    if form.is_valid():
        new_user = form.save(commit=False)
        profile = Profile(user=new_user)

        new_user.save()
        profile.save()
        return new_user
    return None


def update_user_and_profile_by_forms(formUser: UpdateUserForm,
                                     formProfile: UpdateProfileForm) -> bool:
    """
        Обновление информации о пользователе и его профиле

        :param: formUser: UpdateUserForm       - Форма для обновления пользователя
        :param: formProfile: UpdateProfileForm - Форма профиля пользователя
        :return: bool               - Состояние, обновлен ли пользователь или нет
    """
    if formUser.is_valid() and formProfile.is_valid():
        formUser.save()
        formProfile.save()
        return True
    return False
