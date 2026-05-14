import json
import hashlib
from typing import Optional, Any


def make_cache_key(prefix: str, *args) -> str:
    raw = ":".join(str(a) for a in args)
    h = hashlib.md5(raw.encode()).hexdigest()[:16]
    return f"{prefix}:{h}"


async def get_cached(redis, key: str) -> Optional[Any]:
    val = await redis.get(key)
    if val:
        return json.loads(val)
    return None


async def set_cached(redis, key: str, value: Any, ttl: int = 3600):
    await redis.set(key, json.dumps(value), ex=ttl)
