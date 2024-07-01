from django.urls import path
from .views import article, comment


urlpatterns = [
    path('article-list/', article.article_list, name='api-article-list'),
    path('article-list/<int:article_id>/likes', article.article_like, name='api-article-like'),
    path('article-list/<int:article_id>/views', article.article_view, name='api-article-view'),

    path('article-list/<int:article_id>/comments', comment.comment_create_view, name='api-comment-create-list'),
    path('article-list/<int:article_id>/comments/<int:comment_id>/', comment.comment_update_delete, name='api-comment-update-delete'),
]