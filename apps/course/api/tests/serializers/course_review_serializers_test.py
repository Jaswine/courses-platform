from pytest import mark
from apps.course.api.serializers.course_review_serializers import CourseReviewListSerializer


@mark.django_db
def test_course_review_list_serializer_correct_data(course_review_list, course_review):
    """
        Корректные данные
    """
    serializer = CourseReviewListSerializer(course_review_list, many=True)
    data = serializer.data

    assert data is not None
    assert len(data) > 0
    assert data[0].get('id') is course_review.id
    assert data[0].get('message') is course_review.message
    assert data[0].get('user').get('id') is course_review.user.id
    assert data[0].get('user').get('username') is course_review.user.username


@mark.django_db
def test_course_review_list_serializer_empty_list():
    """
        Передача пустого списка
    """
    serializer = CourseReviewListSerializer([], many=True)
    data = serializer.data

    assert data is not None
    assert len(data) == 0
