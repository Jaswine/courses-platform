from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CheckboxSelectMultiple

from apps.user.models import User


class CreateUserForm(UserCreationForm):
    """
        Форма создания пользователя
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(ModelForm):
    """
        Форма обновления данных пользователя
    """
    class Meta:
        model = User
        fields = ['email']

