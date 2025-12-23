"""Redis client initialization and management."""

import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from app.core.config import settings

# Robust retry logic
_REDIS_RETRY = Retry(ExponentialBackoff(), 3)

# Global connection pool with timeouts and health checks
_REDIS_POOL = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=False,
    max_connections=20,
    socket_timeout=5.0,
    socket_connect_timeout=5.0,
    retry_on_timeout=True,
    retry=_REDIS_RETRY,
    health_check_interval=30
)

def get_redis_client() -> redis.Redis:
    """Returns a Redis client from the global connection pool.

    Returns:
        redis.Redis: A Redis client instance.
    """
    return redis.Redis(connection_pool=_REDIS_POOL)
