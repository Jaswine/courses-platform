from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST)
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, IsAdminUser)

from apps.user.api.serializers.achievement_serializers import AchievementSerializer
from apps.user.api.services.achievement_services import find_all_achievements, get_achievement_by_id
from apps.user.models import Achievement


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
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Authentication credentials were not provided.'},
                        status=HTTP_403_FORBIDDEN)


@api_view(['PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def achievement_update(request, achievement_id):
    # Взятие достижения по его идентификатору
    achievement = get_achievement_by_id(achievement_id)
    if achievement is None:
        return Response({'detail': f'Achievement with id: {achievement_id} not found.'},
                        status=HTTP_404_NOT_FOUND)

    serializer = AchievementSerializer(achievement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

