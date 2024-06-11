from django.http import JsonResponse

from article.api.services.article_service import filter_articles, sort_articles
from article.models import ArticleComment


def article_list(request):
    if request.method == 'GET':
        """
            Вывод и фильтрация всех статей
        """
        search = request.GET.get('q', '')
        sorted_by = request.GET.get('sort_by', '')
        tag_list = request.GET.get('tags', '')

        articles = sort_articles(sorted_by, filter_articles(search, tag_list.split('||')))

        articles = [{
            'id': article.id,
            'title': article.title,
            'tags': [{
                'name': tag.name
            } for tag in article.tags.all()],
            'user': article.user.username,
            'likes_count': article.likes.count(),
            'views_count': article.views.count(),
            'liked_for_this_user': True if request.user in article.likes.all() else False,
            'comments_count': ArticleComment.objects.filter(article=article).count(),
            'created': article.created.strftime('%Y-%m-%d %H:%M:%S'),
            'updated': article.updated.strftime('%Y-%m-%d %H:%M:%S'),
        } for article in articles]

        return JsonResponse({
            'status': 'success',
            'articles': articles,
        }, status=200)
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
