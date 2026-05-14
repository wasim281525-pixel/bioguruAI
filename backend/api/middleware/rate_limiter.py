from fastapi import Request, HTTPException, status, Depends
from api.middleware.auth_middleware import get_current_user
from config import settings
import time


async def rate_limit(request: Request, user=Depends(get_current_user)):
    """Redis-backed sliding window rate limiter"""
    redis = request.app.state.redis
    user_id = user.get("sub", "anonymous")
    key = f"rate:{user_id}"

    now = int(time.time())
    window_start = now - settings.RATE_LIMIT_WINDOW

    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, settings.RATE_LIMIT_WINDOW)
    results = await pipe.execute()

    count = results[2]
    if count > settings.RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {settings.RATE_LIMIT_REQUESTS} requests per minute."
        )
    return True
