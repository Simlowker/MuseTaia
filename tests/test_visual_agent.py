"""Tests for the VisualAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.visual_agent import VisualAgent

@pytest.fixture
def mock_genai():
    with patch("app.agents.visual_agent.genai") as mock_gen:
        yield mock_gen

@pytest.fixture
def mock_assets_manager():
    with patch("app.agents.visual_agent.SignatureAssetsManager") as mock_manager:
        yield mock_manager

def test_generate_image_basic(mock_genai, mock_assets_manager):
    """Test basic image generation call."""
    mock_client = mock_genai.Client.return_value
    mock_response = MagicMock()
    mock_response.generated_images = [MagicMock(image_bytes=b"output_image")]
    mock_client.models.generate_images.return_value = mock_response
    
    agent = VisualAgent()
    
    # Mock asset manager returning reference data
    mock_assets_instance = mock_assets_manager.return_value
    mock_assets_instance.download_asset.return_value = b"ref_data"
    
    image_bytes = agent.generate_image(
        prompt="A muse standing in a digital garden",
        subject_id="genesis"
    )
    
    assert image_bytes == b"output_image"
    mock_client.models.generate_images.assert_called_once()
    assert "genesis" in mock_client.models.generate_images.call_args.kwargs["prompt"]
    
    # Verify assets were fetched
    mock_assets_instance.download_asset.assert_called()

def test_initialization(mock_genai, mock_assets_manager):
    """Test initialization of VisualAgent."""
    agent = VisualAgent(model_name="imagen-3.0-generate-001")
    assert agent.model_name == "imagen-3.0-generate-001"
    mock_genai.Client.assert_called_once()
    mock_assets_manager.assert_called_once()
