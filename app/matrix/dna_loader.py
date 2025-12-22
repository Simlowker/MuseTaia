"""Module for loading and initializing the Muse's DNA into the Matrix."""

from typing import Dict, Any
from app.matrix.models import MuseDNA
from app.matrix.context_cache import ContextCacheManager


class DNALoader:
    """Handles the loading of Muse DNA data and its injection into the context cache."""

    def __init__(self, cache_manager: ContextCacheManager):
        """Initializes the DNA loader.

        Args:
            cache_manager: An instance of ContextCacheManager to handle caching.
        """
        self.cache_manager = cache_manager

    def load_dna(self, dna_data: Dict[str, Any]) -> str:
        """Validates DNA data, formats it, and stores it in the Vertex AI Context Cache.

        Args:
            dna_data: A dictionary containing the raw DNA data.

        Returns:
            str: The resource name of the created context cache.
        """
        # Validate data using the MuseDNA model
        dna = MuseDNA(**dna_data)
        
        # Convert to the structured string required for the AI context
        context_string = dna.to_context_string()
        
        # Create the cache (setting a default TTL or using settings)
        # In a real scenario, this DNA cache might have a very long TTL.
        resource_name = self.cache_manager.create_cache(
            content=context_string,
            ttl_seconds=86400 * 7 # 7 days default for DNA
        )
        
        return resource_name
