from unittest.mock import patch, MagicMock
from app.core.config import settings
from app.core.vertex_init import get_genai_client

def test_settings_load():
    assert settings.PROJECT_ID is not None
    assert settings.LOCATION is not None

def test_get_genai_client():
    with patch("google.genai.Client") as mock_client:
        client = get_genai_client()
        assert client is not None
        # Subsequent calls return the same object
        client2 = get_genai_client()
        assert client is client2
