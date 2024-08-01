from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, DateTimeField)

from course.api.serializers.tag_serializers import TagSerializer
from course.api.serializers.title_serializers import TitleListSerializer
from course.api.services.course_review_service import get_course_reviews_count
from course.api.services.course_service import is_user_registered_to_course
from course.api.services.title_service import get_course_titles_by_course_id
from course.models import Course, Title, Task
from user.api.serializers.user_serializers import UserSimpleSerializer


class CourseSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    user = UserSimpleSerializer(read_only=True)
    updated = DateTimeField(format="%Y.%m.%d")
    created = DateTimeField(format="%Y.%m.%d")

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
        fields = CourseSerializer.Meta.fields + ('image', 'comments_count',
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
    titles = SerializerMethodField()
    lessons_count = SerializerMethodField()
    videos_count = SerializerMethodField()
    exercises_count = SerializerMethodField()
    projects_count = SerializerMethodField()
    completed_tasks_count = SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('user_registered', 'titles',
                                                 'lessons_count', 'videos_count',
                                                 'exercises_count', 'projects_count',
                                                 'completed_tasks_count')

    def get_user_registered(self, obj: Course) -> bool:
        user = self.context.get('user')
        return is_user_registered_to_course(obj, user)

    def get_titles(self, obj: Course) -> list[Title]:
        user = self.context.get('user')
        titles = get_course_titles_by_course_id(obj.id)
        return TitleListSerializer(titles, many=True, context={'user': user, 'course': obj}).data

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
