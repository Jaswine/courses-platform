from typing import Any

from celery import shared_task
from django.core.cache import cache

def get_cache(cache_key: str) -> Any | None:
    """
        Взятие данных из кэша по ключу
        :param cache_key: str - Ключ
        :return Any - Данные из кэша или None, если ключ не найден
    """
    return cache.get(cache_key)

def set_cache(cache_key: str, data: Any, /, *, timeout: int = 600) -> None:
    """
        Запись данных в кэш по ключу
        :param cache_key: str - Ключ
        :param data: Any - Данные
        :param timeout: int - Время жизни ключа в секундах (по умолчанию 600 секунд)
    """
    if not isinstance(cache_key, str):
        raise ValueError(f"Ключ кэша должен быть строкой, получен тип {type(cache_key)}")

    if not isinstance(timeout, int) or timeout < 0:
        raise ValueError(f"Время жизни ключа должно быть положительным числом, получено {timeout}")
    try:
        cache.set(cache_key, data, timeout=timeout)
    except Exception as e:
        print(f"Ошибка записи в кэш: {str(e)}")
        raise

def delete_cache_by_key(cache_key: str) -> None:
    """
        Удаление данных из кэша по ключу
        :param cache_key: str - Ключ
    """
    cache.delete(cache_key)

@shared_task
def delete_cache_by_pattern_async(pattern: str) -> None:
    """
        Асинхронное удаление данных из кэша по паттерну ключа.
        :param pattern: str - Паттерн ключа
    """
    cache.delete_pattern(f"{pattern}*")

def delete_cache_by_pattern(pattern: str, /, *, async_mode: bool = False) -> None:
    """
        Удаление данных из кэша по паттерну ключа (началу ключа)
        :param pattern: str - Паттерн ключа
        :param async_mode: bool - Включение асинхронного режима (по умолчанию False)
    """
    pattern = f"{pattern}*"
    if async_mode:
        delete_cache_by_pattern_async(pattern)
    else:
        cache.delete_pattern(pattern)
