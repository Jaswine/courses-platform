from apps.course.api.serializers.title_serializers import TitleSerializer, TitleListSerializer
from pytest import mark


@mark.django_db
def test_title_serializer_many_true(title_list, title_is_public):
    serializer = TitleSerializer(title_list, many=True)
    data = serializer.data

    assert data is not None
    assert len(data) == 2
    assert data[0].get('title') == title_is_public.title
    assert data[0].get('public') == title_is_public.public


@mark.django_db
def test_title_serializer_many_false(title_is_public):
    serializer = TitleSerializer(title_is_public, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('title') == title_is_public.title
    assert data.get('public') == title_is_public.public


@mark.django_db
def test_title_list_serializer_many_true(title_list,
                                         title_is_public,
                                         course_is_public,
                                         user_is_superuser):
    serializer = TitleListSerializer(title_list,
                                     many=True,
                                     context={'user': user_is_superuser,
                                              'course': course_is_public})
    data = serializer.data

    assert data is not None
    assert len(data) == 2
