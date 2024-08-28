from rest_framework.serializers import ModelSerializer

from apps.user.models import Achievement


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description', 'image',
                  'type', 'target_value', 'points',
                  'created')

