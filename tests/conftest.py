"""Fixtures partagées pour tous les tests SMOS v2."""

import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock

@pytest.fixture(scope="session")
def test_images_dir():
    """Retourne le chemin vers les images de test."""
    path = Path(__file__).parent / "fixtures" / "images"
    path.mkdir(parents=True, exist_ok=True)
    return path

@pytest.fixture
def real_redis():
    """Fournit un client Redis réel (nécessite un serveur Redis local)."""
    from app.core.redis_client import get_redis_client
    client = get_redis_client()
    try:
        client.ping()
        yield client
    except Exception:
        pytest.skip("Redis server not available")

@pytest.fixture
def real_genai():
    """Fournit un client GenAI réel (nécessite des credentials GCP)."""
    from app.core.vertex_init import get_genai_client
    client = get_genai_client()
    # On ne fait pas de ping car ça coûte des crédits, 
    # mais on vérifie si les variables d'env sont là
    from app.core.config import settings
    if settings.PROJECT_ID == "placeholder-project-id":
        pytest.skip("GCP Project ID not configured for integration tests")
    yield client