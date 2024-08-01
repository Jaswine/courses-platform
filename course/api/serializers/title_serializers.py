from rest_framework.serializers import ModelSerializer, SerializerMethodField

from course.api.serializers.task_serializers import TaskSimpleSerializer
from course.api.services.task_service import get_tasks_by_title_id
from course.models import Title


class TitleSerializer(ModelSerializer):
    class Meta:
        model = Title
        fields = ('id', 'title', 'public')


class TitleListSerializer(TitleSerializer):
    tasks = SerializerMethodField()

    class Meta(TitleSerializer.Meta):
        model = Title
        fields = TitleSerializer.Meta.fields + ('tasks', )

    def get_tasks(self, obj):
        user = self.context.get('user')
        course = self.context.get('course')
        tasks = get_tasks_by_title_id(obj.id)
        return TaskSimpleSerializer(tasks, many=True, context={'user': user, 'course': course}).data

