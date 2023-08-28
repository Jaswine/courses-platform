from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import FileField, ClearableFileInput
from .models import Profile

class CreateUserForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['username', 'email', 'password1', 'password2']   

class UpdateUserForm(ModelForm):
   class Meta:
      model = User
      fields = ['username', 'email']

class UpdateProfileForm(ModelForm):
   class Meta:
      model = Profile
      fields = ['image', 'location', 'bio', 'number', 'instagram', 'facebook', 'twitter', 'github', 'telegram', 'website']

