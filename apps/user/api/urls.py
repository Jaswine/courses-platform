from django.urls import path

from .views import user

app_name = 'user'

urlpatterns = [
    path('list/', user.user_list, name='user-list'),
    path('<str:username>/<str:info_type>/',
         user.user_view, name='user-view'),
]