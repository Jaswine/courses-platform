from django.urls import path

from .views.auth_view import registration_view, login_view, logout_view
from .views.index_view import index
from .views.tag_view import tag_list_view, tag_delete_view

app_name = 'base'

urlpatterns = [
    path('', index, name='index'),
    
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('tags/', tag_list_view, name='tag_list'),
    path('tags/<int:tag_id>/delete/', tag_delete_view, name='tags-delete'),
]
