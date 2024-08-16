from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.course.api.services.course_service import is_user_registered_to_course
from apps.course.api.services.task_service import task_bookmark_is_exists, is_user_completed_task
from apps.course.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'type', 'points', )


class TaskOneSerializer(ModelSerializer):
    content = SerializerMethodField(read_only=True)
    is_bookmarked = SerializerMethodField(read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('content', 'is_bookmarked', )

    def get_content(self, obj: Task) -> dict:
        """
            Выводит содержимое задания взависимости от типа задания
        """
        content = dict()

        if obj.type == 'TaskText':
            content['text'] = obj.text
        elif obj.type == 'TaskVideo':
            content['video_path'] = obj.video.url if obj.video else None
        elif obj.type == 'TaskProject':
            content['text'] = obj.text

        return content

    def get_is_bookmarked(self, obj: Task) -> bool:
        """
            Проверяет, помечен ли курс или нет
        """
        user = self.context.get('user')
        return task_bookmark_is_exists(obj, user)


class TaskSimpleSerializer(TaskSerializer):
    completed_status = SerializerMethodField(read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ('public', 'completed_status')

    def get_completed_status(self, obj: Task) -> str | None:
        user = self.context.get('user')
        course = self.context.get('course')
        if is_user_registered_to_course(course, user):
            return 'Completed' if is_user_completed_task(obj, user) else 'Uncompleted'
        return None

