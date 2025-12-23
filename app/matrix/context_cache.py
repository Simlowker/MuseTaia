"""Module for managing Vertex AI Context Caching via google-genai SDK."""

import datetime
from typing import Optional, Any, List
import google.genai as genai
from google.genai import types
from app.core.config import settings

class ContextCacheManager:
    """Manages the lifecycle of explicit context caches in Vertex AI.
    
    Used for storing Style Bibles, few-shot examples, and the Matrix DNA
    to reduce latency and costs for long-context interactions.
    """

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )

    def create_explicit_cache(
        self, 
        model_name: str, 
        contents: List[types.Content], 
        ttl_minutes: int = 60
    ) -> str:
        """Creates a new explicit context cache.

        Args:
            model_name: The Gemini model (e.g. 'gemini-1.5-pro-002').
            contents: The data to be cached (System instructions + Examples).
            ttl_minutes: Time to live.

        Returns:
            str: The cache resource name.
        """
        cache = self.client.caches.create(
            model=model_name,
            config=types.CreateCacheConfig(
                contents=contents,
                ttl_seconds=ttl_minutes * 60
            )
        )
        return cache.name

    def get_cache(self, cache_name: str) -> Any:
        """Retrieves a cache object by name."""
        return self.client.caches.get(name=cache_name)

    def delete_cache(self, cache_name: str) -> None:
        """Deletes a context cache."""
        self.client.caches.delete(name=cache_name)