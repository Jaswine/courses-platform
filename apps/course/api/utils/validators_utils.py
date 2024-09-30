

def full_number_validator(page: int) -> int:
    """
        Валидации страницы для пагинатора при взятии ее

        :param page: int - Страница
        :return Страница или ошибка
    """
    try:
        return abs(int(page))
    except ValueError:
        return 1