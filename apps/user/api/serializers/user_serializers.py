from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User

from apps.user.models import Profile


class UserSimpleSerializer(ModelSerializer):
    ava = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'ava')

    def get_ava(self, obj) -> str:
        return obj.profile.image.url if obj.profile.image else ''


class UserSerializer(UserSimpleSerializer):
    scores = SerializerMethodField()

    class Meta(UserSimpleSerializer.Meta):
        fields = UserSimpleSerializer.Meta.fields + ('email',
                                                     'is_superuser', 'is_active',
                                                     'scores')

    def get_scores(self, obj) -> int:
        return obj.profile.scores


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('scores',
                  'image', 'backImage',
                  'bio', 'location',
                  'Twitter', 'GitHub', 'GitLub', 'Linkedin', 'Telegram', 'website',
                  'skills', 'interests')
