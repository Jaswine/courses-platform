from django.contrib.auth.models import User
from pytest import mark

from apps.course.api.serializers.task_serializers import TaskSerializer, TaskOneSerializer
from apps.course.models import Task


@mark.django_db
def test_task_serializer_many_is_true(task_list: list,
                                      task_is_public: Task):
    serializer = TaskSerializer(task_list, many=True)
    data = serializer.data

    assert data is not None
    assert len(data) == 2
    assert data[1].get('id') == task_is_public.id
    assert data[1].get('title') == task_is_public.title
    assert data[1].get('type') == task_is_public.type
    assert data[1].get('points') == task_is_public.points


@mark.django_db
def test_task_serializer_many_is_false(task_is_public: Task):
    serializer = TaskSerializer(task_is_public, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == task_is_public.id
    assert data.get('title') == task_is_public.title
    assert data.get('type') == task_is_public.type
    assert data.get('points') == task_is_public.points


@mark.django_db
def test_task_one_serializer_text_user_bookmarked(task_is_public: Task,
                                                  user_is_not_superuser: User):
    serializer = TaskOneSerializer(task_is_public,
                                   many=False,
                                   context={'user': user_is_not_superuser})
    data = serializer.data

    assert data is not None
    assert data.get('id') == task_is_public.id
    assert data.get('title') == task_is_public.title
    assert data.get('type') == task_is_public.type
    assert data.get('points') == task_is_public.points
    assert data.get('content').get('text') == task_is_public.text
    assert data.get('is_bookmarked') is True


@mark.django_db
def test_task_one_serializer_video_is_not_none_user_not_bookmarked(task_video: Task):
    serializer = TaskOneSerializer(task_video,
                                   many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == task_video.id
    assert data.get('title') == task_video.title
    assert data.get('type') == task_video.type
    assert data.get('points') == task_video.points
    assert data.get('content').get('video_path') == task_video.video.url
    assert data.get('is_bookmarked') is False


@mark.django_db
def test_task_one_serializer_video_is_none_user_not_bookmarked(task_video: Task):
    task_video.video = None

    serializer = TaskOneSerializer(task_video, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == task_video.id
    assert data.get('title') == task_video.title
    assert data.get('type') == task_video.type
    assert data.get('points') == task_video.points
    assert data.get('content').get('video_path') == None
    assert data.get('is_bookmarked') is False


@mark.django_db
def test_task_one_serializer_project_user_not_bookmarked(task_project: Task):
    serializer = TaskOneSerializer(task_project, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == task_project.id
    assert data.get('title') == task_project.title
    assert data.get('type') == task_project.type
    assert data.get('points') == task_project.points
    assert data.get('content').get('text') == task_project.text
    assert data.get('is_bookmarked') is False


