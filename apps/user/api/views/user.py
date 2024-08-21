from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from apps.user.api.serializers.user_serializers import UserSerializer
from apps.user.services.user_service import get_user_by_username


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_main_info(request, username: str):
    user = get_user_by_username(username)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=HTTP_200_OK)