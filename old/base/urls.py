from django.urls import path

from .views.auth_view import registration_view, login_view, logout_view
from .views.index_view import index
from .views.tag_view import tag_list_view, tag_delete_view
from .views.profile import profile, profile_courses_view, profile_articles_view, profile_likes_view,profile_update_view, profile_sertificates

app_name = 'base'

urlpatterns = [
    path('', index, name='index'),
    
    # Auth
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Tags
    path('tags/', tag_list_view, name='tag_list'),
    path('tags/<int:tag_id>/delete/', tag_delete_view, name='tags-delete'),
    
    # Profile
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/likes', profile_likes_view, name='profile-likes'),
    path('profile/<str:username>/courses', profile_courses_view, name='profile-courses'),
    path('profile/<str:username>/articles', profile_articles_view, name='profile-articles'),
    path('profile/<str:username>/change', profile_update_view  , name='profile-update'),    
    path('profile/<str:username>/profile_sertificates', profile_sertificates, name='profile-sertificates'),
]
