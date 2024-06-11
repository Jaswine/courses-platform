from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from article.models import Article, ArticleComment


def comment_create_view(request, article_id: int) -> JsonResponse:
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'GET':
        """
            Вывод всех комментариев
        """
        comments = ArticleComment.objects.filter(article=article)
        comments = [{
            'id': comment.id,
            'message': comment.message,
        } for comment in comments]

        return JsonResponse({
            'status': 'success',
            'data': comments
        }, status=200)

    elif request.method == 'POST':
        """
            Создание нового комментария
        """
        return JsonResponse({
            'status': 'success',
        }, status=201)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


def comment_update_delete(request, article_id, comment_id) -> JsonResponse:
    article = get_object_or_404(Article, pk=article_id)
    comment = get_object_or_404(ArticleComment, pk=comment_id)

    if request.method == 'POST':
        """
            Обновление комментария
        """
        return JsonResponse({
            'status': 'success',

        }, status=200)

    elif request.method == 'DELETE':
        """
            Удаление комментария
        """
        comment.delete()
        return JsonResponse({}, status=204)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)
