"""Tests for the SearchService."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.services.search_service import SearchService

@pytest.fixture
def mock_genai():
    with patch("app.core.services.search_service.genai") as mock_gen:
        yield mock_gen

def test_search_execution(mock_genai):
    """Test that search calls the model with the correct tool config."""
    mock_client = mock_genai.Client.return_value
    mock_response = MagicMock()
    mock_response.text = "Paris Fashion Week is currently ongoing."
    mock_client.models.generate_content.return_value = mock_response
    
    service = SearchService()
    result = service.search("What is happening at Paris Fashion Week?")
    
    assert result == "Paris Fashion Week is currently ongoing."
    
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args
    assert call_args.kwargs["contents"] == "What is happening at Paris Fashion Week?"
    
    # Verify tool usage
    tools = call_args.kwargs["config"].tools
    assert len(tools) == 1
    # Check if google_search is present in the tool definition
    # Note: Structure depends on SDK internals, usually it's an object
    assert tools[0].google_search is not None

def test_get_grounding_metadata(mock_genai):
    """Test retrieval of grounding metadata."""
    mock_client = mock_genai.Client.return_value
    mock_response = MagicMock()
    
    mock_metadata = MagicMock()
    mock_candidate = MagicMock()
    mock_candidate.grounding_metadata = mock_metadata
    mock_response.candidates = [mock_candidate]
    
    mock_client.models.generate_content.return_value = mock_response
    
    service = SearchService()
    metadata = service.get_search_grounding_metadata("query")
    
    assert metadata == mock_metadata