import time
from typing import Any, Dict, Tuple

_cache: Dict[Tuple[str, str], Tuple[float, Any]] = {}


def get_cached(source: str, ticker: str, ttl_seconds: int) -> Any:
    key = (source, ticker.upper())
    entry = _cache.get(key)
    if not entry:
        return None
    ts, value = entry
    if time.time() - ts > ttl_seconds:
        _cache.pop(key, None)
        return None
    return value


def set_cached(source: str, ticker: str, value: Any) -> None:
    key = (source, ticker.upper())
    _cache[key] = (time.time(), value)
