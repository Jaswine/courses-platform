from django.urls import path
from .views import auth, main, user

app_name = 'auth'


urlpatterns = [
    path('sign-in/', auth.sign_in, name='sign-in'),
    path('sign-up/', auth.sign_up, name='sign-up'),
    path('sign-out/', auth.sign_out, name='sign-out'),   
   
    path('', main.dashboard, name='dashboard'),
    path('favorites/', main.favorites, name='favorites'),   
    
    path('settings/', user.settings, name='settings'),
    path('users/<str:username>/', user.profile, name='profile'),
    path('users/<str:username>/certificates/', user.certificates, name='certificates'),
    
]
