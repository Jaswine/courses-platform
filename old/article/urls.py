from django.urls import path
from .views import get_all_articles_list, create_article, show_article, update_article, delete_article, delete_comment

app_name = 'article'

urlpatterns = [
    path('', get_all_articles_list, name='all_articles'),
    path('create', create_article, name='create_article'),
    
    path('<str:slug>', show_article, name='show_article'),
    path('<str:slug>/update', update_article, name='update_article'),
    path('<str:slug>/delete', delete_article, name='delete_article'),
    
    path('<str:slug>/comments/<int:id>/', delete_comment, name='delete_comment')
]
