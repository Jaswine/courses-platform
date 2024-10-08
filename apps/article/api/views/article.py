from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django.views.decorators.csrf import csrf_exempt

from apps.article.api.services.article_reaction_service import toggle_reaction
from apps.article.api.services.article_service import find_articles_by_user_status, search_articles_by_title, \
    filter_articles_by_tags, sort_articles
from apps.article.api.services.article_view_service import add_view_to_article
from apps.article.api.utils.collect_article_data_util import collect_article_data_utils
from apps.article.models import Article
from apps.course.api.utils.get_element_or_404 import get_element_or_404
from apps.user.models import Reaction


def article_list(request):
    if request.method == 'GET':
        """
            Вывод и фильтрация всех статей
        """
        search = request.GET.get('q', '')
        sorted_by = request.GET.get('sort_by', '')
        tag_list = request.GET.get('tags', '')

        articles = find_articles_by_user_status(request.user.is_superuser)
        articles = search_articles_by_title(search, articles)
        articles = filter_articles_by_tags(tag_list.split(','), articles)
        articles = sort_articles(sorted_by, articles)

        articles = collect_article_data_utils(articles)

        return JsonResponse({
            'status': 'success',
            'articles': articles,
        }, status=200)
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


@require_http_methods(["POST"])
def article_comment_react(request, article_id: int):
    """
        Реакция на комментарии
    """
    if request.user.is_authenticated:
        article = get_element_or_404(Article, article_id)
        if isinstance(article, JsonResponse):
            return article

        reaction_type = request.data.get('reaction_type')

        if reaction_type not in dict(Reaction.REACTION_CHOICES).keys():
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid reaction type! {reaction_type} not found!'
            }, status=400)

        response_message = toggle_reaction(article, request.user, reaction_type)

        return JsonResponse({
            'status': 'success',
            'message': response_message
        }, status=201)
    return JsonResponse({
        'status': 'error',
        'message': 'User is not authenticated!'
    }, status=401)


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
            message = add_view_to_article(article, request.user)

            return JsonResponse({
                'status': 'success',
                'message': message
            }, status=200)
        return JsonResponse({
            'status': 'error',
            'message': 'User is not authenticated!'
        }, status=401)
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed!'
    }, status=405)
