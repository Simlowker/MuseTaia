"""Centralized initialization for Google GenAI Client."""

import google.genai as genai
from app.core.config import settings

# Global Singleton
_GENAI_CLIENT = None

def get_genai_client() -> genai.Client:
    """Initializes and returns the GenAI client singleton.
    
    Dynamically switches between Vertex AI (GCP) and standard API Key 
    based on the presence of GOOGLE_API_KEY.
    """
    global _GENAI_CLIENT
    
    if _GENAI_CLIENT is not None:
        return _GENAI_CLIENT

    if settings.GOOGLE_API_KEY and "AIza" in settings.GOOGLE_API_KEY:
        # Standard AI Studio Mode (Simpler for local/hybrid tests)
        _GENAI_CLIENT = genai.Client(api_key=settings.GOOGLE_API_KEY)
    else:
        # Industrial Vertex AI Mode (GCP Native)
        _GENAI_CLIENT = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
    
    return _GENAI_CLIENT