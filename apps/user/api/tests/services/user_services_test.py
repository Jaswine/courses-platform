from pytest import mark

from apps.user.api.services.user_services import find_all_users, search_users, filter_users_by_is_active, \
    filter_users_by_is_superuser, sort_users, filter_search_sort_users, block_user
from apps.user.models import User


@mark.django_db
def test_find_all_users(user_list):
    """
        Взятие всех пользователей
    """
    users = find_all_users()

    assert users is not None
    assert len(user_list) == len(users)
    assert user_list[0] in users
    assert user_list[1] in users

@mark.django_db
@mark.parametrize("search_field", ['username', 'first_name', 'last_name', 'email'])
def  test_search_users_by_username(user_list, search_field):
    """
        Сортировка пользователей, пользователь найден
    """
    search_value = getattr(user_list[0], search_field)
    users = search_users(User.objects.all(), search_value)

    assert users is not None
    assert len(users) == 1
    assert user_list[0] in users
    assert getattr(users[0], search_field) == search_value

@mark.django_db
def test_search_users_no_results(user_list):
    """
        Сортировка пользователей, пользователь не найден
    """
    users = search_users(User.objects.all(), 'sdfpnvpwdnfwdfj')

    assert users is not None
    assert len(users) == 0


@mark.django_db
@mark.parametrize("status", [True, False])
def test_filter_users_by_is_active(user_list, status):
    """
       Фильтрация пользователей по наличию статуса активности
    """
    users = filter_users_by_is_active(User.objects.all(), status)

    assert users is not None
    assert len(users) == 3


@mark.django_db
@mark.parametrize("status", [True, False])
def test_filter_users_by_is_superuser(user_list, status):
    """
        Фильтрация пользователей по наличию статуса суперпользователя
    """
    users = filter_users_by_is_superuser(User.objects.all(), status)

    assert users is not None
    assert len(users) == 3


@mark.django_db
@mark.parametrize("order_by", ['Newest', 'Oldest', 'Many points', 'Few points', 'Another Word'])
def test_sort_users(user_list, order_by):
    """
        Сортировка пользователей
    """
    users = sort_users(User.objects.all(), order_by)

    assert users is not None
    assert len(user_list) == len(users)
    match order_by:
        case 'Newest' | 'Many points':
            assert user_list[0] == users[len(users) - 1]
            assert user_list[-1] == users[0]
        case 'Oldest' | 'Few points' | 'Another Word':
            assert user_list[0].username == users[0].username
            assert user_list[:1] ==  users[:1]


@mark.django_db
def test_filter_search_sort_users(user_list):
    # Без каких-либо фильтров или сортировки
    users = filter_search_sort_users()
    assert len(users) == len(user_list)

    # Поиск
    users = filter_search_sort_users(search="user1")
    assert len(users) == 1
    assert users[0].username == "user1"

    # Фильтрация по наличию статуса активности
    users = filter_search_sort_users(is_active=True)
    assert users is not None
    assert len(users) == 3

    # Фильтрация по наличию статуса суперпользователя
    users = filter_search_sort_users(is_superuser=True)
    assert users is not None
    assert len(users) == 3

    # Cортировка по новинкам
    users = filter_search_sort_users(order_by="Newest")
    assert users[0].username == user_list[len(user_list) - 1].username

    # Сортировка по наибольшему количеству очков
    users = filter_search_sort_users(order_by="Many points")
    assert users[0].username == user_list[len(user_list) - 1].username


@mark.django_db
def test_block_user(user_list):
    # Блокировка пользователя
    message = block_user(user_list[1])
    assert message is not None
    assert message == 'Пользователь успешно заблокирован'

    # Разблокировка пользователя
    message = block_user(user_list[0])
    assert message is not None
    assert message == 'Пользователь успешно разблокирован'
