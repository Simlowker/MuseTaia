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

    def load_dna(self, dna_data: Dict[str, Any], model_name: str = "gemini-1.5-pro-002") -> str:
        """Validates DNA data, formats it, and stores it in the Vertex AI Context Cache.

        Args:
            dna_data: A dictionary containing the raw DNA data.
            model_name: The model to create the cache for.

        Returns:
            str: The resource name of the created context cache.
        """
        # Validate data using the MuseDNA model
        dna = MuseDNA(**dna_data)
        
        # Convert to the structured string required for the AI context
        context_string = dna.to_context_string()
        
        # Create the 'Bible' cache with 7 days TTL
        resource_name = self.cache_manager.create_bible_cache(
            model_name=model_name,
            system_instruction=context_string,
            examples=[], # Could be populated with viral patterns in the future
            ttl_days=7
        )
        
        return resource_name
