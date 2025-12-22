"""Service for performing web searches using Google Search via GenAI SDK."""

from typing import List, Dict, Any, Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings

class SearchService:
    """Wrapper for Google Search capabilities."""

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """Initializes the SearchService.

        Args:
            model_name: Model to use for grounding/summarizing.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    def search(self, query: str) -> str:
        """Performs a search and returns a summarized answer based on results.

        Args:
            query: The search query.

        Returns:
            str: The grounded answer.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=query,
            config=types.GenerateContentConfig(
                tools=[self.search_tool],
                response_modalities=["TEXT"]
            )
        )
        
        # Extract the text and any grounding metadata if needed
        # For now, we return the text which is grounded in the search results
        return response.text

    def get_search_grounding_metadata(self, query: str) -> Optional[types.GroundingMetadata]:
        """Performs a search and returns the grounding metadata (sources).

        Args:
            query: The search query.

        Returns:
            GroundingMetadata: Structured source info.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=query,
            config=types.GenerateContentConfig(
                tools=[self.search_tool],
                response_modalities=["TEXT"]
            )
        )
        
        # Access candidates[0].grounding_metadata
        if response.candidates and response.candidates[0].grounding_metadata:
            return response.candidates[0].grounding_metadata
        return None
