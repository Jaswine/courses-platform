from django.urls import path
from article.views import article

app_name = 'article'

urlpatterns = [
    path('', article.article_list_view, name='article_list'),
    path('create/', article.create_article_view, name='create_article'),
    path('<int:id>/', article.article_detail_view, name='article_detail'),
    path('<int:id>/edit/', article.update_article_view, name='update_article'),
    path('<int:id>/delete/', article.delete_article_view, name='delete_article'),
]
