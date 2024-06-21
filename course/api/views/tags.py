from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..services.TagService import create_new_tag, get_all_tags, filter_tags_by_name, get_tag_by_id, delete_tag_by_id, \
    update_tag
from ..utils.extract_tag_data_util import extract_tag_data_util
from ...models import Tag
from ...utils import checking_slug, slug_generator


@csrf_exempt
def tags_list_create(request):
    if request.method == 'GET':
        """
            Показ всех тэгов
        """
        # Берем данные
        query = request.GET.get('q', '')
        tags = get_all_tags()

        # Проверяем длину поисковой строки
        if query and len(query) > 2:
            # Фильтруем данные
            tags = filter_tags_by_name(tags, query)

        return JsonResponse({
            'status': 'success',
            'tags': extract_tag_data_util(tags)
        }, safe=False, status=200)
    elif request.method == 'POST':
        if request.user.is_superuser:
            """
                Создание нового тега
            """
            # Берем названия тэга
            name = request.POST.get('name', '')

            # Создаем новый тэг
            tag = create_new_tag(name)

            return JsonResponse({
                'id': tag.id,
                'name': tag.name
            }, status=201)
        else:
            return JsonResponse({
                "status": "error",
                "message": "Access denied for this user: you don't have any permission to create a new tag."
            }, status=403)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Access denied for this method: This method seems to be illegal in this world.',
        }, status=405)


@csrf_exempt
def tags_get_update_delete(request, id: int):
    try:
        # Берем тэг по id
        tag = get_tag_by_id(id)
    except Tag.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': f'Name tag: {id} not found.'
        }, status=404)

    if request.method == 'PUT':
        """
            Обновление тэга
        """
        # Берем названия тэга
        name = request.POST.get('name', '')

        # Обновляем тэг
        update_tag(tag, name)

        return JsonResponse({
            'status': 'success',
            'message': 'Tag updated successfully!'
        }, status=200)

    elif request.method == 'DELETE':
        """
            Удаление тэга
        """
        delete_tag_by_id(tag)

        return JsonResponse({
            'status': 'success',
            'message': 'Tag deleted successfully!'
        }, status=204)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Access denied for this method: This method seems to be illegal in this world.'
        },status=405)
