from django.contrib.auth.models import User
from pytest import mark, fixture

from user.forms import UpdateUserForm, CreateUserForm, UpdateProfileForm
from user.models import Profile
from user.services.user_service import get_user_by_email, get_user_by_username, create_user_and_profile_by_form, \
    update_user_and_profile_by_forms


@fixture
def valid_data_create_user_form():
    form_data = {
        'username': 'test',
        'email': 'test@example.com',
        'password1': '12345test.1234',
        'password2': '12345test.1234',
    }
    return CreateUserForm(form_data)


@fixture
def valid_data_update_user_form(user):
    form_data = {
        'email': 'test1@gmail.com',
    }
    return UpdateUserForm(data=form_data,
                          instance=user)


@fixture
def valid_data_update_profile_form(profile):
    form_data = {
        'image': None,
        'bio': 'Test description',
        'location': 'Some location',
        'skills': [],
        'interests': [],
        'Twitter': 'https://twitter.com/test',
        'GitHub': 'https://github.com/test',
        'GitLub': 'https://gitlub.com/test',
        'Linkedin': 'https://www.linkedin.com/in/test',
        'Telegram': 'https://t.me/test',
        'website': 'https://test.com',
    }
    return UpdateProfileForm(data=form_data,
                             instance=profile)


@mark.django_db
def test_get_user_by_email_success(user):
    """
        Взятие пользователя по электронной почте
    """
    current_user = get_user_by_email(user.email)

    assert current_user is not None
    assert current_user.username == user.username
    assert current_user.email == user.email


@mark.django_db
def test_get_user_by_email_user_not_found(user):
    """
        Взятие пользователя по электронной почте,
                                    пользователь не найден
    """
    current_user = get_user_by_email('none@gmail.com')

    assert current_user is None


@mark.django_db
def test_get_user_by_username(user):
    """
        Взятие пользователя по имени пользователя
    """
    current_user = get_user_by_username(user.username)

    assert current_user is not None
    assert current_user.username == user.username
    assert current_user.email == user.email


@mark.django_db
def test_get_user_by_username_user_not_found(user):
    """
        Взятие пользователя по имени пользователя,
                                        пользователь не найден
    """
    current_user = get_user_by_username('none')

    assert current_user is None


@mark.django_db
def test_create_user_and_profile_by_form_valid_data(valid_data_create_user_form):
    """
        Создание пользователя с его профиля, используя форму,
                                            правильные тестовые данные
    """
    user = create_user_and_profile_by_form(valid_data_create_user_form)

    assert user is not None
    assert user.username == valid_data_create_user_form.cleaned_data['username']
    assert user.email == valid_data_create_user_form.cleaned_data['email']
    assert Profile.objects.count() == 1
    assert Profile.objects.filter(user=user).exists()


@mark.django_db
def test_create_user_and_profile_by_form_invalid_data():
    """
        Создание пользователя с его профиля, используя форму,
                                            неправильные тестовые данные
    """
    form = CreateUserForm(data={})
    user = create_user_and_profile_by_form(form)

    assert user is None
    assert Profile.objects.count() == 0


@mark.django_db
def test_update_user_by_form_valid_data(valid_data_update_user_form, valid_data_update_profile_form):
    """
        Обновление данных пользователя, правильные тестовые данные
    """
    user = update_user_and_profile_by_forms(valid_data_update_user_form,
                                            valid_data_update_profile_form)

    assert user is True
    assert User.objects.get(id=1).email == valid_data_update_user_form.cleaned_data['email']
    assert Profile.objects.get(id=1).bio == valid_data_update_profile_form.cleaned_data['bio']
    assert Profile.objects.get(id=1).location == valid_data_update_profile_form.cleaned_data['location']
    assert Profile.objects.get(id=1).GitHub == valid_data_update_profile_form.cleaned_data['GitHub']


@mark.django_db
def test_update_user_by_form_valid_data(user, profile):
    """
        Обновление данных пользователя, правильные тестовые данные
    """
    update_user_form = UpdateUserForm(data=None, instance=user)
    update_profile_form = UpdateProfileForm(data=None, instance=profile)

    user = update_user_and_profile_by_forms(update_user_form, update_profile_form)

    assert user is False
    assert User.objects.get(id=1).email == 'user@example.com'
