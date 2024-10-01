from typing import Any
from django.core.cache import cache

def get_cache(cache_key: str) -> Any:
    return cache.get(cache_key)

def set_cache(cache_key: str, data: Any, /, *, timeout: int = 600):
    cache.set(cache_key, data, timeout=timeout)

def delete_cache_by_key(cache_key: str):
    cache.delete(cache_key)

def delete_cache_by_pattern(pattern: str):
    cache.delete_pattern(f"{pattern}*")
