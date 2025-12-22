"""Tests for the DirectorAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.director_agent import DirectorAgent
from app.core.schemas.screenplay import ShotType, CameraMovement

@pytest.fixture
def mock_genai():
    with patch("app.agents.director_agent.genai") as mock_gen:
        yield mock_gen

def test_generate_video(mock_genai):
    """Test video generation call with cinematic controls."""
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
        image_bytes=b"reference_image",
        shot_type=ShotType.CLOSE_UP,
        camera_movement=CameraMovement.ZOOM_IN
    )
    
    assert video_bytes == b"generated_video_content"
    mock_client.models.generate_videos.assert_called_once()
    call_args = mock_client.models.generate_videos.call_args
    assert "Shot type: close_up" in call_args.kwargs["prompt"]
    assert "Camera movement: zoom_in" in call_args.kwargs["prompt"]
    assert "A digital muse walking in a garden" in call_args.kwargs["prompt"]
    assert call_args.kwargs["image"].image_bytes == b"reference_image"

def test_generate_video_with_multi_references(mock_genai):
    """Test video generation with multiple reference images (Ingredients-to-Video)."""
    mock_client = mock_genai.Client.return_value
    mock_operation = MagicMock()
    mock_video = MagicMock()
    mock_video.video_bytes = b"multi_ref_video"
    mock_operation.result.return_value = MagicMock(generated_videos=[mock_video])
    mock_client.models.generate_videos.return_value = mock_operation
    
    agent = DirectorAgent()
    
    references = [
        (b"char_bytes", "ASSET"),
        (b"style_bytes", "STYLE")
    ]
    
    video_bytes = agent.generate_video(
        prompt="Character dancing",
        reference_images=references
    )
    
    assert video_bytes == b"multi_ref_video"
    call_args = mock_client.models.generate_videos.call_args
    config = call_args.kwargs["config"]
    assert len(config.reference_images) == 2
    assert config.reference_images[0].reference_type == "ASSET"
    assert config.reference_images[1].reference_type == "STYLE"

def test_initialization(mock_genai):
    """Test initialization."""
    agent = DirectorAgent(model_name="veo-3.1")
    assert agent.model_name == "veo-3.1"
    mock_genai.Client.assert_called_once()
