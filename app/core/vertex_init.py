"""Centralized initialization for Google GenAI Client."""

import google.genai as genai
from app.core.config import settings

def get_genai_client() -> genai.Client:
    """Initializes and returns the GenAI client.
    
    Dynamically switches between Vertex AI (GCP) and standard API Key 
    based on the presence of GOOGLE_API_KEY.
    """
    if settings.GOOGLE_API_KEY and "AIza" in settings.GOOGLE_API_KEY:
        # Standard AI Studio Mode (Simpler for local/hybrid tests)
        return genai.Client(api_key=settings.GOOGLE_API_KEY)
    else:
        # Industrial Vertex AI Mode (GCP Native)
        return genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )