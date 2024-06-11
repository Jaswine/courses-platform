from django.urls import path
from .views import article_list, comment


urlpatterns = [
    path('article-list/', article_list.article_list, name='api-article-list'),
]