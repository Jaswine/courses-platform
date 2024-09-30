from typing import Any
from django.core.cache import cache
from django_redis import get_redis_connection


def get_cache(cache_key: str) -> Any:
    return cache.get(cache_key)

def set_cache(cache_key: str, data: dict | list, /, *, timeout: int = 600):
    cache.set(cache_key, data, timeout=timeout)

def delete_cache_by_key(cache_key: str):
    cache.delete(cache_key)

def delete_cache_by_keys(cache_key: str):
    conn = get_redis_connection('default')
    # Посмотреть все ключи из терминала !!!
    print("CONN: ", conn)
    keys = conn.scan_iter(f'{cache_key}*')
    print("cache_key: ", cache_key)
    print("KEYS FOR DELETING: ", keys)

    for key in keys:
        print("key: ", key)

    # if keys:
    #     conn.delete(*keys)
