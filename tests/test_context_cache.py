import pytest
from unittest.mock import MagicMock, patch
from app.matrix.context_cache import ContextCacheManager

@pytest.fixture
def mock_genai():
    with patch("app.matrix.context_cache.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_create_cache_success(mock_genai):
    manager = ContextCacheManager()
    
    # Mock the returned cache object
    mock_cache_instance = MagicMock()
    mock_cache_instance.name = "projects/123/locations/us-central1/cachedContents/456"
    mock_genai.caches.create.return_value = mock_cache_instance
    
    result_name = manager.create_bible_cache("gemini-1.5-pro", "System", ["Ex 1"], ttl_days=1)
    
    assert result_name == "projects/123/locations/us-central1/cachedContents/456"
    mock_genai.caches.create.assert_called_once()

def test_get_cache_status(mock_genai):
    manager = ContextCacheManager()
    
    mock_cache_instance = MagicMock()
    mock_cache_instance.name = "test-cache"
    mock_genai.caches.get.return_value = mock_cache_instance
    
    cache_obj = manager.get_cache("projects/123/locations/us-central1/cachedContents/456")
    assert cache_obj.name == "test-cache"
    mock_genai.caches.get.assert_called_with(name="projects/123/locations/us-central1/cachedContents/456")

def test_delete_cache(mock_genai):
    manager = ContextCacheManager()
    cache_name = "projects/123/locations/us-central1/cachedContents/456"
    
    manager.delete_cache(cache_name)
    
    mock_genai.caches.delete.assert_called_with(name=cache_name)
