from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User


class UserSimpleSerializer(ModelSerializer):
    ava = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'ava']

    def get_ava(self, obj):
        return obj.profile.image.url if obj.profile.image else ''
