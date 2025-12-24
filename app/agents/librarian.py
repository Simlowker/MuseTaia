"""Librarian Agent for viral structure extraction and semantic retrieval."""

import logging
import json
import google.genai as genai
from google.genai import types
from typing import List, Optional, Any, Dict
from app.core.config import settings
from app.core.vertex_init import get_genai_client

logger = logging.getLogger(__name__)

class Librarian:
    """Agent that manages the Muse's 'Experience Memory'.
    
    This agent represents the 'Perception Lobe's' memory specialist.
    It specializes in deconstructing successful content into its DNA (structural patterns)
    and retrieving relevant past experiences to inform current creativity.
    """

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        """Initializes the Librarian.
        
        Args:
            model_name: The name of the model to use for analysis.
        """
        self.client = get_genai_client()
        self.model_name = model_name

    def extract_viral_structure(self, content: str) -> Dict[str, Any]:
        """Deconstructs content into its underlying structural components.        
        Args:
            content: The text, script, or description to analyze.
            
        Returns:
            Dict: A structural map of the content.
        """
        prompt = f"""
        Analyze the following content and extract its 'Viral DNA' structure.
        Identify the underlying mechanics that make it effective.
        
        Content:
        {content}
        
        Return a JSON object with:
        - narrative_skeleton: The core arc (e.g., Hook -> Build -> Payoff).
        - psychological_triggers: Why it resonates (e.g., FOMO, curiosity, validation).
        - aesthetic_anchors: Key visual or tonal markers.
        - viral_score: Estimated virality from 1-10.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.warning(f"LIBRARIAN: Failed to parse JSON response: {e}. Raw: {response.text[:200]}")
            return {"raw_analysis": response.text, "parse_error": str(e)}
        except Exception as e:
            logger.error(f"LIBRARIAN: Unexpected error during viral extraction: {e}")
            raise

    def get_embeddings(self, text: str) -> List[float]:
        """Generates embeddings for the given text.
        
        Args:
            text: The text to embed.
            
        Returns:
            List[float]: The embedding vector.
        """
        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embeddings[0].values

    def semantic_search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Performs a semantic search for relevant experiences.
        
        Currently implemented as a conceptual mock for Vertex AI Vector Search.
        """
        # In a real implementation:
        # 1. Generate query embedding: self.get_embeddings(query)
        # 2. Query Vertex AI Vector Search Index.
        # 3. Return top-k matches.
        
        return [
            {
                "content": f"Past successful campaign about {query} from October 2025.",
                "relevance": 0.95,
                "tags": ["success", "viral", "identity_match"]
            }
        ][:limit]
