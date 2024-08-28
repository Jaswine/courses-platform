from rest_framework.serializers import ModelSerializer

from apps.user.models import Achievement


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('title', 'description', 'image',
                  'type', 'target_value', 'points',
                  'created')

