from django.http import JsonResponse

from article.api.services.article_service import filter_articles, sort_articles
from django.views.decorators.csrf import csrf_exempt
from article.models import ArticleComment, Article
from course.api.utils.get_element_or_404 import get_element_or_404


def article_list(request):
    if request.method == 'GET':
        """
            Вывод и фильтрация всех статей
        """
        search = request.GET.get('q', '')
        sorted_by = request.GET.get('sort_by', '')
        tag_list = request.GET.get('tags', '')

        print(tag_list)
        articles = sort_articles(sorted_by, filter_articles(request.user.is_superuser, search, tag_list.split(',')))

        articles = [{
            'id': article.id,
            'title': article.title,
            'image': article.image.url if article.image else None,
            'tags': [{
                'id': tag.id,
                'name': tag.name,
            } for tag in article.tags.all()],
            'user': article.user.username,
            'likes_count': article.reactions.count(),
            'comments_count': ArticleComment.objects.filter(article=article).count(),
            'created': article.created.strftime('%d.%m.%Y'),
            'updated': article.updated.strftime('%d.%m.%Y'),
        } for article in articles]

        return JsonResponse({
            'status': 'success',
            'articles': articles,
        }, status=200)
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


@csrf_exempt
def article_like(request, article_id: int):
    """
        Добавление и удаление лайков
    """
    article = get_element_or_404(Article, id=article_id)
    if isinstance(article, JsonResponse):
        return article

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user in article.likes.all():
                article.likes.remove(request.user)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Like removed successfully!'
                }, status=200)
            else:
                article.likes.add(request.user)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Like added successfully!'
                }, status=200)

        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed!'
        }, status=405)

    return JsonResponse({
        'status': 'error',
        'message': 'User unauthenticated!'
    }, status=403)


@csrf_exempt
def article_view(request, article_id: int):
    """
        Добавление просмотров
    """
    article = get_element_or_404(Article, id=article_id)
    if isinstance(article, JsonResponse):
        return article

    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user not in article.views.all():
                article.views.add(request.user)

                return JsonResponse({
                    'status': 'success',
                    'message': 'View added successfully!'
                }, status=200)
        else:
            print('REQUEST: ', request)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed!'
    }, status=405)
