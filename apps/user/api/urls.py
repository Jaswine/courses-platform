from django.urls import path

from .views.user import UserInfoView

app_name = 'user'

urlpatterns = [
    path('<str:username>/<str:info_type>/', UserInfoView.as_view(), name='user-info'),
]