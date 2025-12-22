"""Tests for the EICAgent."""

import pytest
import json
from unittest.mock import MagicMock, patch
from app.agents.eic_agent import EICAgent

@pytest.fixture
def mock_assets_manager():
    with patch("app.agents.eic_agent.SignatureAssetsManager") as mock_manager:
        yield mock_manager.return_value

def test_stage_for_review(mock_assets_manager):
    """Verifies that the EIC stages video, poster, and metadata correctly."""
    agent = EICAgent()
    
    production_data = {
        "title": "My Awesome Post",
        "caption": "Check this out! #cool",
        "video_bytes": b"video_data",
        "poster_image_bytes": b"poster_data"
    }
    
    path = agent.stage_for_review(production_data, "genesis")
    
    assert "reviews/genesis/" in path
    
    # Check that upload_asset was called for all 3 components
    assert mock_assets_manager.upload_asset.call_count == 3
    
    # Check metadata upload specifically
    calls = mock_assets_manager.upload_asset.call_args_list
    metadata_call = next(c for c in calls if "metadata.json" in c.args[0])
    uploaded_json = json.loads(metadata_call.args[1].decode("utf-8"))
    assert uploaded_json["title"] == "My Awesome Post"
