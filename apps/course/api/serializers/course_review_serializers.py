from rest_framework.serializers import ModelSerializer, DateTimeField, SerializerMethodField, ImageField
from django.contrib.auth.models import User

from apps.course.models import CourseReview
from apps.user.api.serializers.user_serializers import UserSimpleSerializer


class CourseReviewListSerializer(ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    updated = DateTimeField(format="%Y.%m.%d %H:%M:%S", read_only=True)
    created = DateTimeField(format="%Y.%m.%d %H:%M:%S", read_only=True)

    class Meta:
        model = CourseReview
        fields = ['id', 'message', 'stars', 'user', 'updated', 'created']
