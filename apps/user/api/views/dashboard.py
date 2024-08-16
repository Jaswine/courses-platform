from django.http import JsonResponse
from apps.course.models import Course


def registered_courses(request):
    """
        Вывод курсов на которые подписан человек
    """
    if request.user.is_authenticated:
        courses = Course.objects.filter(users_who_registered=request.user)

        # data = generate_courses_list_util(request.user, courses)

        return JsonResponse({
            'status': 'success',
            # 'courses': data,
        }, status=200)

    return JsonResponse({
        'status': 'error',
        'message': 'You are not logged in.'
    }, status=401)
