from django.urls import path
from .views import article, comment


urlpatterns = [
    path('article-list/', article.article_list, name='api-article-list'),
    path('article-list/<int:article_id>/likes', article.article_like, name='api-article-like'),
    path('article-list/<int:article_id>/views', article.article_view, name='api-article-view'),
]