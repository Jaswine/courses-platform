from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.user.models import User


class UserBaseSerializer(ModelSerializer):
    """
        Базовый сериализатор,
            включающий email и пароль
    """
    class Meta:
        model = User
        fields = ('email', 'password', )


class UserSerializer(UserBaseSerializer):
    """
        Обычный сериализатор,
            включающий email, пароль и имя пользователя
    """
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ('username', )


class UserSimpleSerializer(UserSerializer):
    """
        Простой сериализатор,
            включающий email, пароль, имя пользователя,
                                        его id и путь к аватарке
    """
    ava = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('id', 'ava', )

    def get_ava(self, obj) -> str:
        return obj.image.url if obj.image else ''


class UserProfileSerializer(UserSimpleSerializer):
    """
        Профильный сериализатор
    """
    class Meta(UserSimpleSerializer.Meta):
        fields = UserSimpleSerializer.Meta.fields + ('email', 'scores',
                                                     'is_superuser', 'is_blocked',
                                                     'image', 'backImage', 'bio', 'location', )
