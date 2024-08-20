from apps.course.api.serializers.course_serializers import CreateCourseSerializer


def create_course_by_serializer(data, user):
    serializer = CreateCourseSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return serializer.data, None
    return None, serializer.errors