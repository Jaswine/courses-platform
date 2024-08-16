from apps.course.api.serializers.tag_serializers import TagSerializer
from pytest import mark


@mark.django_db
def test_tag_serializer_many_true(tag_list, tag1, tag2):
    serializer = TagSerializer(tag_list, many=True)
    data = serializer.data

    assert data is not None
    assert len(data) == 2
    assert data[0].get('id') == tag1.id
    assert data[0].get('name') == tag1.name


@mark.django_db
def test_tag_serializer_many_false(tag1):
    serializer = TagSerializer(tag1, many=False)
    data = serializer.data

    assert data is not None
    assert data.get('id') == tag1.id
    assert data.get('name') == tag1.name

