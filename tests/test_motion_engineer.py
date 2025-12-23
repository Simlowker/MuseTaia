"""Tests for the MotionEngineer agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.motion_engineer import MotionEngineer

@pytest.fixture
def mock_genai():
    with patch("google.genai.Client") as mock_gen:
        yield mock_gen

def test_motion_engineer_handoff(mock_genai):
    mock_client = mock_genai.return_value
    mock_operation = MagicMock()
    mock_response = MagicMock()
    mock_video = MagicMock()
    mock_video.video_bytes = b"fake_video_bytes"
    mock_response.generated_videos = [mock_video]
    mock_operation.result.return_value = mock_response
    mock_client.models.generate_videos.return_value = mock_operation
    
    engineer = MotionEngineer()
    video = engineer.execute_cinematic_handoff(
        b"start", b"end", "Zoom into details"
    )
    
    assert video == b"fake_video_bytes"
    assert mock_client.models.generate_videos.called
    call_args = mock_client.models.generate_videos.call_args
    assert "Smooth cinematic transition" in call_args.kwargs["prompt"]
