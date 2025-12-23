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
        subject_id="genesis",
        location_id="paris_studio",
        object_ids=["blue_sofa"],
        item_ids=["neon_jacket"]
    )
    
    assert image_bytes == b"output_image"
    mock_client.models.generate_images.assert_called_once()
    prompt_used = mock_client.models.generate_images.call_args.kwargs["prompt"]
    assert "genesis" in prompt_used
    assert "paris_studio" in prompt_used
    assert "blue_sofa" in prompt_used
    assert "neon_jacket" in prompt_used
    
    # Verify assets were fetched
    # Should be called for subject face, location ref, object ref, and wardrobe ref
    assert mock_assets_instance.download_asset.call_count >= 4

def test_initialization(mock_genai, mock_assets_manager):

    """Test initialization of VisualAgent."""

    agent = VisualAgent(model_name="imagen-3.0-generate-001")

    assert agent.model_name == "imagen-3.0-generate-001"

    mock_genai.Client.assert_called_once()

    mock_assets_manager.assert_called_once()



def test_edit_image(mock_genai, mock_assets_manager):



    """Test image editing with inpainting."""



    mock_client = mock_genai.Client.return_value



    mock_response = MagicMock()

    mock_response.generated_images = [MagicMock(image_bytes=b"edited_image")]

    mock_client.models.edit_image.return_value = mock_response

    

    agent = VisualAgent()

    

    base_img = b"base_image"

    mask_img = b"mask_image"

    

    edited_bytes = agent.edit_image(

        prompt="Add sunglasses",

        base_image_bytes=base_img,

        mask_image_bytes=mask_img

    )

    

    assert edited_bytes == b"edited_image"

    mock_client.models.edit_image.assert_called_once()

    

    # Check args

    call_args = mock_client.models.edit_image.call_args

    assert call_args.kwargs["prompt"] == "Add sunglasses"

    refs = call_args.kwargs["reference_images"]

    assert len(refs) == 2 # Raw + Mask


