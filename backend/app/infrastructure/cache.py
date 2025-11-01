import time
from typing import Any, Callable, Optional
from .settings import settings


class InMemoryTTLCache:
    def __init__(self, default_ttl_seconds: int | None = None) -> None:
        self._store: dict[str, tuple[float, Any]] = {}
        self._default_ttl = default_ttl_seconds or settings.cache_ttl_seconds

    def get(self, key: str) -> Any:
        record = self._store.get(key)
        if not record:
            return None
        expires_at, value = record
        if expires_at < time.time():
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds or self._default_ttl
        self._store[key] = (time.time() + ttl, value)

    def cached(self, key_builder: Callable[..., str], ttl_seconds: Optional[int] = None):
        def decorator(func: Callable[..., Any]):
            async def wrapper(*args, **kwargs):
                key = key_builder(*args, **kwargs)
                cached_value = self.get(key)
                if cached_value is not None:
                    return cached_value
                value = await func(*args, **kwargs)
                self.set(key, value, ttl_seconds)
                return value
            return wrapper
        return decorator


cache = InMemoryTTLCache()


