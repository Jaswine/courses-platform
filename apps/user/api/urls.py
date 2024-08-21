from django.urls import path

from .views import user

app_name = 'user'

urlpatterns = [
    path('<str:username>/',
         user.user_main_info, name='user-main-info'),
]