"""Tests for the StylistAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.stylist_agent import StylistAgent
from app.matrix.wardrobe_dna import WardrobeRegistry
from app.matrix.models import WardrobeItem, SceneProp
from app.core.schemas.look import LookSelection
from app.core.schemas.world import SceneLayout
from app.state.models import Mood

@pytest.fixture
def mock_genai():
    with patch("app.agents.stylist_agent.genai") as mock_gen:
        yield mock_gen

@pytest.fixture
def wardrobe_registry():
    registry = WardrobeRegistry()
    registry.register_item(WardrobeItem(
        item_id="neon_jacket", name="Neon Jacket", description="...", visual_reference_path="...", tags=["cyberpunk"]
    ))
    registry.register_prop(SceneProp(
        prop_id="camera", name="Camera", description="...", visual_reference_path="..."
    ))
    return registry

def test_select_look(mock_genai, wardrobe_registry):
    """Test that the agent selects an outfit correctly."""
    mock_client = mock_genai.Client.return_value
    
    # Mock Response
    mock_selection = LookSelection(
        item_ids=["neon_jacket"],
        prop_ids=["camera"],
        stylist_note="Perfect for a high-tech night scene.",
        visual_details="The neon strips on the jacket pulse slowly."
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_selection
    mock_client.models.generate_content.return_value = mock_response
    
    agent = StylistAgent()
    layout = SceneLayout(location_id="tokyo_street", scene_description="Night street")
    mood = Mood(valence=0.7, arousal=0.8)
    
    selection = agent.select_look("She is documenting the street fashion", layout, mood, wardrobe_registry)
    
    assert "neon_jacket" in selection.item_ids
    assert "camera" in selection.prop_ids
    mock_client.models.generate_content.assert_called_once()
