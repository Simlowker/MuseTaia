"""Vertex AI initialization and utility functions."""

from google.cloud import aiplatform
from app.core.config import settings


def init_vertex_ai():
    """Initializes the Vertex AI SDK with project settings."""
    aiplatform.init(
        project=settings.PROJECT_ID,
        location=settings.LOCATION,
    )
