from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, DateTimeField,
                                        PrimaryKeyRelatedField)

from apps.course.api.serializers.tag_serializers import TagSerializer
from apps.course.api.services.course_review_service import get_course_reviews_count
from apps.course.api.services.course_service import is_user_registered_to_course
from apps.course.api.services.tag_service import get_all_tags
from apps.course.models import Course, Title, Task
from apps.user.api.serializers.user_serializers import UserSimpleSerializer


class CourseSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = UserSimpleSerializer(read_only=True)
    updated = DateTimeField(format="%Y.%m.%d", read_only=True)
    created = DateTimeField(format="%Y.%m.%d", read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'user', 'tags',
                  'updated', 'created',)


class CourseListSerializer(CourseSerializer):
    image = SerializerMethodField()
    likes = SerializerMethodField()
    comments_count = SerializerMethodField()
    liked_for_this_user = SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('image', 'reviews_count',
                                                 'likes', 'liked_for_this_user',)

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return get_course_reviews_count(obj)

    def get_liked_for_this_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False


class CourseOneSerializer(CourseSerializer):
    user_registered = SerializerMethodField()
    lessons_count = SerializerMethodField()
    videos_count = SerializerMethodField()
    exercises_count = SerializerMethodField()
    projects_count = SerializerMethodField()
    completed_tasks_count = SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('image', 'about',
                                                 'user_registered',
                                                 'lessons_count', 'videos_count',
                                                 'exercises_count', 'projects_count',
                                                 'completed_tasks_count')

    def get_user_registered(self, obj: Course) -> bool:
        user = self.context.get('user')
        return is_user_registered_to_course(obj, user)

    def __get_task_count_by_type(self, obj: Course, task_type: str = None) -> int:
        if task_type:
            return Task.objects.filter(
                titles__courses=obj,
                type=task_type,
                public=True
            ).distinct().count()
        return Task.objects.filter(
            titles__courses=obj,
            public=True
        ).distinct().count()

    def get_lessons_count(self, obj: Course) -> int:
        return self.__get_task_count_by_type(obj)

    def get_videos_count(self, obj: Course) -> int:
        return self.__get_task_count_by_type(obj, 'TaskVideo')

    def get_exercises_count(self, obj: Course) -> int:
        return self.__get_task_count_by_type(obj, 'TaskCode')

    def get_projects_count(self, obj: Course) -> int:
        return self.__get_task_count_by_type(obj, 'TaskProject')

    def get_completed_tasks_count(self, obj: Course) -> int:
        user = self.context.get('user')
        return Task.objects.filter(
            titles__courses=obj,
            users_who_completed__username=user.username
        ).distinct().count()


class CreateCourseSerializer(CourseSerializer):
    tags = PrimaryKeyRelatedField(many=True, queryset=get_all_tags())

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('image', 'about',
                                                 'public')


class CourseProgressSerializer(CourseSerializer):
    progress = SerializerMethodField()
    image = SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('image', 'progress')

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_progress(self, obj):
        user = self.context.get('user')

        tasks_count = Task.objects.filter(titles__courses=obj,
                                          public=True).distinct().count()
        completed_tasks_count = Task.objects.filter(titles__courses=obj,
                                                    users_who_completed__username=user.username
                                                    ).distinct().count()

        return '{}%'.format(completed_tasks_count * 100 / tasks_count
                            if tasks_count != 0 and completed_tasks_count != 0 else 0)
