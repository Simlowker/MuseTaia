"""Tests for the VideoStreamHandler."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.handlers.visual_stream import VideoStreamHandler

@pytest.fixture
def mock_genai():
    with patch("app.agents.handlers.visual_stream.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

@pytest.mark.asyncio
async def test_describe_frame(mock_genai):
    """Test that describe_frame correctly calls Gemini and returns text."""
    mock_client = mock_genai
    
    mock_response = MagicMock()
    mock_response.text = "A person walking in a park."
    # mock_client.aio.models.generate_content is an async method
    mock_client.aio.models.generate_content = AsyncMock(return_value=mock_response)
    
    handler = VideoStreamHandler()
    description = await handler.describe_frame(b"fake_frame_data")
    
    assert description == "A person walking in a park."
    mock_client.aio.models.generate_content.assert_called_once()
    
    # Check parts
    call_args = mock_client.aio.models.generate_content.call_args
    parts = call_args.kwargs["contents"][0].parts
    assert len(parts) == 2
    assert parts[0].inline_data.data == b"fake_frame_data"

def test_summarize_stream_window():
    """Test summarizing multiple frame descriptions."""
    handler = VideoStreamHandler()
    descriptions = ["Person enters", "Person waves", "Person leaves"]
    summary = handler.summarize_stream_window(descriptions)
    
    assert "Person waves" in summary
    assert "activity" in summary
