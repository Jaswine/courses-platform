from pytest import mark

from apps.course.api.serializers.course_serializers import CourseSerializer, CourseListSerializer, CourseOneSerializer


@mark.django_db
def test_course_serializer_many_is_true(course_list, course_is_public):
    serializer = CourseSerializer(course_list, many=True)
    data = serializer.data

    assert data is not None
    assert len(data) > 0
    assert data[0].get('id') == course_is_public.id
    assert data[0].get('title') == course_is_public.title
    assert data[0].get('user').get('id') == course_is_public.user.id
    assert data[0].get('user').get('username') == course_is_public.user.username
    assert len(data[0].get('tags')) == course_is_public.tags.count()


@mark.django_db
def test_course_serializer_many_is_false(course_is_public):
    serializer = CourseSerializer(course_is_public, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == course_is_public.id
    assert data.get('title') == course_is_public.title
    assert data.get('user').get('id') == course_is_public.user.id
    assert data.get('user').get('username') == course_is_public.user.username
    assert len(data.get('tags')) == course_is_public.tags.count()


@mark.django_db
def test_course_list_serializer_correct_data_context_user_liked(course_list, course_is_public, user_is_not_superuser):
    serializer = CourseListSerializer(course_list, many=True, context={'user': user_is_not_superuser})
    data = serializer.data

    assert data is not None
    assert len(data) > 0
    assert data[0].get('id') == course_is_public.id
    assert data[0].get('title') == course_is_public.title
    assert data[0].get('user').get('id') == course_is_public.user.id
    assert data[0].get('user').get('username') == course_is_public.user.username
    assert data[0].get('image') is None
    assert data[0].get('comments_count') == 0
    assert data[0].get('likes') == 1
    assert data[0].get('liked_for_this_user') is True


@mark.django_db
def test_course_list_serializer_correct_data_context_user_didnt_liked(course_list,
                                                                      course_is_public,
                                                                      user_is_superuser):
    serializer = CourseListSerializer(course_list, many=True, context={'user': user_is_superuser})
    data = serializer.data

    assert data is not None
    assert len(data) > 0
    assert data[0].get('id') == course_is_public.id
    assert data[0].get('title') == course_is_public.title
    assert data[0].get('user').get('id') == course_is_public.user.id
    assert data[0].get('user').get('username') == course_is_public.user.username
    assert data[0].get('image') is None
    assert data[0].get('comments_count') == 0
    assert data[0].get('likes') == 1
    assert data[0].get('liked_for_this_user') is False


@mark.django_db
def test_course_one_serializer(course_is_public, user_is_not_superuser):
    serializer = CourseOneSerializer(course_is_public,
                                     many=False,
                                     context={'user': user_is_not_superuser})
    data = serializer.data

    assert data is not None
    assert len(data) > 0
    assert data.get('id') == course_is_public.id
    assert data.get('title') == course_is_public.title
    assert data.get('user').get('id') == course_is_public.user.id
    assert data.get('user').get('username') == course_is_public.user.username
    assert data.get('user_registered') is True
    assert data.get('lessons_count') == 0
    assert data.get('videos_count') == 0
    assert data.get('exercises_count') == 0
    assert data.get('projects_count') == 0
    assert data.get('completed_tasks_count') == 0


