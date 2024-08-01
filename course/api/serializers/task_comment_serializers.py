from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, DateTimeField,
                                        IntegerField, BooleanField)

from course.api.services.task_comment_service import task_comment_like_count, task_comment_like_is_exist
from course.models import TaskComment
from user.api.serializers.user_serializers import UserSimpleSerializer


class TaskCommentSerializer(ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    message = SerializerMethodField()
    created = DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    updated = DateTimeField(format='%H:%M %d.%m.%Y', read_only=True)
    is_liked = BooleanField(default=False, read_only=True)
    likes_count = IntegerField(default=0, read_only=True)

    class Meta:
        model = TaskComment
        fields = ('id', 'user', 'message', 'created', 'updated',
                  'is_liked', 'likes_count', )

    def get_message(self, obj: TaskComment) -> str:
        return obj.text

    def get_is_liked(self, obj: TaskComment) -> bool:
        user = self.context.get('user')
        return task_comment_like_is_exist(obj, user)

    def get_likes_count(self, obj: TaskComment) -> int:
        return task_comment_like_count(obj)


class TaskCommentListSerializer(TaskCommentSerializer):
    depth = IntegerField(default=0, read_only=True)
    children = SerializerMethodField(read_only=True)

    class Meta(TaskCommentSerializer.Meta):
        fields = TaskCommentSerializer.Meta.fields + ('depth', 'children')

    def get_children(self, obj: TaskComment) -> [TaskComment]:
        if obj.task_comment_children.count() > 0:
            depth = self.context.get('depth', 0) + 1
            children_serializer = TaskCommentListSerializer(
                obj.task_comment_children.all(),
                many=True,
                context={'user': self.context.get('user'), 'depth': depth}
            )
            return children_serializer.data
        return None


