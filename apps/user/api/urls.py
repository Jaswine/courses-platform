from django.urls import path

from .views import user, achievement

app_name = 'user'

urlpatterns = [
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