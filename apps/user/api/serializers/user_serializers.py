from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.user.models import User


class UserSimpleSerializer(ModelSerializer):
    ava = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'ava')

    def get_ava(self, obj) -> str:
        return obj.image.url if obj.image else ''


class UserSerializer(UserSimpleSerializer):
    class Meta(UserSimpleSerializer.Meta):
        fields = UserSimpleSerializer.Meta.fields + ('email', 'scores',
                                                     'is_superuser', 'is_blocked',
                                                     'image', 'backImage', 'bio', 'location', )
