from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, IsAdminUser)

from apps.user.api.serializers.achievement_serializers import AchievementSerializer
from apps.user.api.services.achievement_services import find_all_achievements


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def achievement_list_create(request):
    if request.method == 'GET':
        achievements = find_all_achievements()
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    if request.method == 'POST':
        if request.user.is_superuser:
            serializer = AchievementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_404_NOT_FOUND)
        return Response({'detail': 'Authentication credentials were not provided.'},
                        status=HTTP_403_FORBIDDEN)
