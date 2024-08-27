from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_405_METHOD_NOT_ALLOWED,
                                   HTTP_403_FORBIDDEN, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from rest_framework.response import Response

from ..serializers.tag_serializers import TagSerializer
from ..services.tag_service import find_tags_by_name, create_tag, get_tag_by_id, delete_tag, update_tag_name


@api_view(['GET', 'POST'])
def tag_create_list(request):
    """
        TODO: Вывод списка тэгов и создание нового тэга
    """
    if request.method == 'GET':
        # Берем запрос для поиска
        query = request.GET.get('q', '')
        # Берем все тэги
        tags = find_tags_by_name(query)
        # Выводим тэги
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data,
                        status=HTTP_200_OK)

    if request.method == 'POST':
        if request.user.is_superuser:
            # Берем название тэга
            name = request.data.get('name', '')
            # Проверяем тэг на существование
            if find_tags_by_name(name):
                return Response({'detail': 'Tag already exists'}, status=HTTP_400_BAD_REQUEST)
            # Создаем новый тэг
            tag = create_tag(name)
            # Выводим тэг
            serializer = TagSerializer(tag, many=False)
            return Response(serializer.data,
                            status=HTTP_201_CREATED)
        return Response({'detail': 'User doesn\'t have sufficient rights'}, status=HTTP_403_FORBIDDEN)
    return Response({'detail': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def tags_get_update_delete(request, id: int):
    """
        Просмотр, обновление и удаление тэга
    """
    tag = get_tag_by_id(id)

    if not tag:
        return Response({'detail': f'Tag with ID: {id} not found.'}, status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Выводим тэг
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=HTTP_200_OK)

    if not request.user.is_superuser:
        return Response({'detail': 'You don\'t have enough privileges'}, status=HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        # Берем новое название тэга
        tag_name = request.data.get('name', '')
        # Проверяем на существование
        if not tag_name or find_tags_by_name(tag_name):
            return Response({'detail': 'Tag already exists'}, status=HTTP_400_BAD_REQUEST)
        # Обновляем
        update_tag_name(tag_name, tag)
        return Response({'detail': 'Tag updated successfully'}, status=HTTP_200_OK)

    if request.method == 'DELETE':
        # Удаляем тэг
        delete_tag(tag)
        return Response({}, status=HTTP_204_NO_CONTENT)

    return Response({'detail': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)

