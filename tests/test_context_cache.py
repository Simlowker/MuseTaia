import pytest
from unittest.mock import MagicMock, patch
from app.matrix.context_cache import ContextCacheManager

@pytest.fixture
def mock_vertex_cache():
    # Patch the aiplatform module where it is imported in the code under test
    with patch("app.matrix.context_cache.aiplatform") as mock_aiplatform:
        # Mock the CachedContent class within the mocked module
        mock_cached_content = MagicMock()
        mock_aiplatform.CachedContent = mock_cached_content
        yield mock_cached_content

def test_create_cache_success(mock_vertex_cache):
    manager = ContextCacheManager()
    
    content = "This is the Muse DNA backstory."
    
    # Mock the returned cache object
    mock_cache_instance = MagicMock()
    mock_cache_instance.name = "projects/123/locations/us-central1/cachedContents/456"
    mock_vertex_cache.create.return_value = mock_cache_instance
    
    result_name = manager.create_cache(content, ttl_seconds=3600)
    
    assert result_name == "projects/123/locations/us-central1/cachedContents/456"
    mock_vertex_cache.create.assert_called_once()

def test_get_cache_status(mock_vertex_cache):
    manager = ContextCacheManager()
    
    mock_cache_instance = MagicMock()
    mock_cache_instance.name = "test-cache"
    mock_vertex_cache.get.return_value = mock_cache_instance
    
    cache_obj = manager.get_cache("projects/123/locations/us-central1/cachedContents/456")
    assert cache_obj.name == "test-cache"
    mock_vertex_cache.get.assert_called_with("projects/123/locations/us-central1/cachedContents/456")

def test_delete_cache(mock_vertex_cache):
    manager = ContextCacheManager()
    cache_name = "projects/123/locations/us-central1/cachedContents/456"
    
    mock_cache_instance = MagicMock()
    mock_vertex_cache.get.return_value = mock_cache_instance
    
    manager.delete_cache(cache_name)
    
    mock_vertex_cache.get.assert_called_with(cache_name)
    mock_cache_instance.delete.assert_called_once()
