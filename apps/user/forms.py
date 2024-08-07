from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CheckboxSelectMultiple

from django.contrib.auth.models import User
from .models import Profile


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


class UpdateProfileForm(ModelForm):
    """
           Форма обновления данных профиля пользователя
    """
    class Meta:
        model = Profile
        fields = ['image',
                  'bio', 'location',
                  'skills', 'interests',
                  'Twitter', 'GitHub', 'GitLub', 'Linkedin', 'Telegram', 'website',
                  'skills', 'interests']
        widgets = {
            'skills': CheckboxSelectMultiple,
            'interests': CheckboxSelectMultiple,
        }
