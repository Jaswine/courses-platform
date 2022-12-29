from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('articles', views.articleList, name='article_list'),
    path('create-articles', views.createArticle, name='create_article'),
]
