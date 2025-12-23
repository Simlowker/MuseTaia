"""Redis client initialization and management."""

import redis
from app.core.config import settings

# Global connection pool
_REDIS_POOL = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=False,
    max_connections=20
)

def get_redis_client() -> redis.Redis:
    """Returns a Redis client from the global connection pool.

    Returns:
        redis.Redis: A Redis client instance.
    """
    return redis.Redis(connection_pool=_REDIS_POOL)
