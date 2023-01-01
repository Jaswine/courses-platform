from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('articles', views.articleList, name='article_list'),
    path('create-articles', views.createArticle, name='create_article'),
    path('articles/<str:slug>/', views.showArticle, name='show_article'),
    path('articles/<str:slug>/delete', views.deleteArticle, name='delete_article'),
    path('articles/<str:slug>/update', views.updateArticle, name='update_article'),
    
]
