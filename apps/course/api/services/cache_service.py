from typing import Any

from celery import shared_task
from django.core.cache import cache

from apps.course.api.utils.logger_util import logger


def get_cache(cache_key: str) -> Any | None:
    '''
        Взятие данных из кэша по ключу
        :param cache_key: str - Ключ
        :return Any - Данные из кэша или None, если ключ не найден
    '''
    logger.delay(f'Кэш успешно взят по ключу: {cache_key}', 'info')
    return cache.get(cache_key)

def set_cache(cache_key: str, data: Any, /, *, timeout: int = 600) -> None:
    '''
        Запись данных в кэш по ключу
        :param cache_key: str - Ключ
        :param data: Any - Данные
        :param timeout: int - Время жизни ключа в секундах (по умолчанию 600 секунд)
    '''
    if not isinstance(cache_key, str):
        raise ValueError(f'Ключ кэша должен быть строкой, получен тип {type(cache_key)}')

    if not isinstance(timeout, int) or timeout < 0:
        raise ValueError(f'Время жизни ключа должно быть положительным числом, получено {timeout}')
    try:
        cache.set(cache_key, data, timeout=timeout)
        logger.delay(f'Кэш успешно записан: {cache_key} - {timeout} секунд', 'info')
    except Exception as e:
        logger.delay(f'Ошибка записи в кэш: {str(e)}', 'error')
        raise

def delete_cache_by_key(cache_key: str) -> None:
    '''
        Удаление данных из кэша по ключу
        :param cache_key: str - Ключ
    '''
    cache.delete(cache_key)
    logger.delay(f'Кэш успешно удален: {cache_key}', 'info')


@shared_task(bind=True, max_retries=3)
def delete_cache_by_pattern_async(pattern: str) -> None:
    '''
        Асинхронное удаление данных из кэша по паттерну ключа.
        :param pattern: str - Паттерн ключа
    '''
    cache.delete_pattern(pattern)
    logger.delay(f'Кэш успешно асинхронно удален по паттерну: {pattern}', 'info')


def delete_cache_by_pattern(pattern: str, /, *, async_mode: bool = True) -> None:
    '''
        Удаление данных из кэша по паттерну ключа (началу ключа)
        :param pattern: str - Паттерн ключа
        :param async_mode: bool - Включение асинхронного режима (по умолчанию False)
    '''
    pattern = f'{pattern}*'
    if async_mode:
        delete_cache_by_pattern_async.delay(pattern)
    else:
        cache.delete_pattern(pattern)
        logger.delay(f'Кэш успешно удален по паттерну: {pattern}', 'info')
