from django.urls import path
from .  import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    
    #! REGISTRATION & LOGIN & LOGOUT
    path('sign-up', views.registration, name='registration'),
    path('sign-in', views.loginUser, name='login'),
    path('sign-out', views.logoutUser, name='logout'),
    
    #! TAGS 
    path('tags', views.listTags, name='tags'),
    path('tags/<str:id>/', views.deleteTag, name='tags-delete'),
    
    #! USER
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/courses', views.profileCourses, name='profile-courses'),
    path('profile/<str:username>/articles', views.profileArticles, name='profile-articles'),
    path('profile/<str:username>/change', views.profileUpdate  , name='profile-update'),
]
