from apps.course.models import CourseReview
from statistics import median


def calculate_median_stars_util(reviews: list[CourseReview]) -> float:
    """
        Вычисляет медианное значение звёзд из списка отзывов.

        :param reviews: List[Review] - Список отзывов
        :return float - Медианное значение звёзд
    """
    stars = [review.stars for review in reviews]
    return round(median(stars) if stars else 0, 2)
