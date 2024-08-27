from rest_framework.serializers import ModelSerializer

from apps.user.models import Achievement


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('title', 'description',
                  'type', 'target_value', 'image',
                  'created')

