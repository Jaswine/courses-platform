from django.urls import path
from article.views import article

app_name = 'article'

urlpatterns = [
    path('', article.article_list, name='article_list'),
    path('<int:id>/', article.article_detail, name='article_detail'),
    path('create/', article.create_article, name='create_article'),
    path('<int:id>/update/', article.update_article, name='update_article'),
    path('<int:id>/delete/', article.delete_article, name='delete_article'),
]