from unittest.mock import patch
from app.core.config import settings
from app.core.vertex_init import init_vertex_ai

def test_settings_load():
    assert settings.PROJECT_ID is not None
    assert settings.LOCATION is not None

def test_init_vertex_ai():
    with patch("google.cloud.aiplatform.init") as mock_init:
        init_vertex_ai()
        mock_init.assert_called_once_with(
            project=settings.PROJECT_ID,
            location=settings.LOCATION,
        )
