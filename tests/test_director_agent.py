"""Tests for the DirectorAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.director_agent import DirectorAgent

@pytest.fixture
def mock_genai():
    with patch("app.agents.director_agent.genai") as mock_gen:
        yield mock_gen

def test_generate_video(mock_genai):
    """Test video generation call."""
    mock_client = mock_genai.Client.return_value
    
    # Mock the LRO (Long Running Operation)
    mock_operation = MagicMock()
    mock_video = MagicMock()
    mock_video.video_bytes = b"generated_video_content"
    mock_operation.result.return_value = MagicMock(generated_videos=[mock_video])
    mock_client.models.generate_videos.return_value = mock_operation
    
    agent = DirectorAgent()
    video_bytes = agent.generate_video(
        prompt="A digital muse walking in a garden",
        image_bytes=b"reference_image"
    )
    
    assert video_bytes == b"generated_video_content"
    mock_client.models.generate_videos.assert_called_once()
    call_args = mock_client.models.generate_videos.call_args
    assert call_args.kwargs["prompt"] == "A digital muse walking in a garden"
    assert call_args.kwargs["image"].image_bytes == b"reference_image"

def test_initialization(mock_genai):
    """Test initialization."""
    agent = DirectorAgent(model_name="veo-3.1")
    assert agent.model_name == "veo-3.1"
    mock_genai.Client.assert_called_once()
