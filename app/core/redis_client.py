"""Redis client initialization and management."""

import redis
from app.core.config import settings


def get_redis_client() -> redis.Redis:
    """Creates and returns a Redis client based on application settings.

    Returns:
        redis.Redis: A Redis client instance.
    """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=False,  # Return bytes for binary data compatibility
    )
