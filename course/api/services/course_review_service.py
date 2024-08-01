from django.contrib.auth.models import User

from course.models import Course, CourseReview


def get_course_reviews(course: Course) -> list[CourseReview]:
    """
        Взятие всех отзывов курса

        :param course: Course - Курс
        :return list[CourseReview] - Отзывы курса
    """
    return CourseReview.objects.filter(course=course)


def get_course_reviews_count(course: Course) -> int:
    """
        Взятие колличества всех отзывов для курса

        :param course: Course - Курс
        :return int - Колличество отзывов курса
    """
    return CourseReview.objects.filter(course=course).count()


def get_course_review_by_id(id: int) -> CourseReview | None:
    """
        Взятие отзыва к курсу по id

        :param id: int - Идентификатор отзыва к курсу
        :return CourseReview | None  - Отзыв к курсу
    """
    try:
        return CourseReview.objects.get(id=id)
    except CourseReview.DoesNotExist:
        return None


def filter_course_reviews_by_user(course: Course, user: User) -> list[CourseReview]:
    """
        Фильтрация отзывов по курсу и пользователю

        :param course: Course - Курс
        :param user: User - Пользователь
        :return list[Course] - Список отзывов
    """
    return CourseReview.objects.filter(course=course,
                                       user=user)


def create_course_review(course: Course,
                         user: User,
                         message: str,
                         stars_count: int) -> CourseReview:
    """
        Создание отзыва

        :param course: Course - Курс
        :param user: User - Пользователь
        :param message: str - Сообщение
        :param stars_count: int - Колличество звезд
        :return CourseReview - Отзыв курса
    """
    return CourseReview.objects.create(
        user=user,
        course=course,
        message=message,
        stars=stars_count
    )


def delete_course_review(review: CourseReview):
    """
        Удаление отзыва

        :param review: CourseReview - Отзыв
    """
    review.delete()
