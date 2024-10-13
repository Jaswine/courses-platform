from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import user, achievement, auth


app_name = 'user'

urlpatterns = [
    path('sign-in/', auth.sign_in, name='sign-in'),
    path('sign-up/', auth.sign_up, name='sign-up'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('achievement-list/',
         achievement.achievement_list_create, name='achievement-list-create'),
    path('achievement-list/<int:achievement_id>/',
         achievement.achievement_update, name='achievement-update'),
    
    path('list/', user.user_list, name='user-list'),
    path('<str:username>/block/',
         user.user_add_remove_block_status, name='user-add-remove-block-status'),
    path('<str:username>/<str:info_type>/',
         user.user_view, name='user-view'),
]