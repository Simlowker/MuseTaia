"""Tests for the ArchitectAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.architect_agent import ArchitectAgent
from app.matrix.world_dna import WorldRegistry
from app.matrix.models import WorldLocation, WorldObject
from app.core.schemas.world import SceneLayout

@pytest.fixture
def mock_genai():
    with patch("app.agents.architect_agent.genai") as mock_gen:
        yield mock_gen

@pytest.fixture
def world_registry():
    registry = WorldRegistry()
    registry.register_object(WorldObject(
        object_id="blue_sofa", name="Blue Sofa", description="...", visual_reference_path="..."
    ))
    registry.register_location(WorldLocation(
        location_id="paris_studio", name="Paris Studio", description="...", 
        visual_reference_path="...", lighting_setup="...", recurring_objects=["blue_sofa"]
    ))
    return registry

def test_plan_scene_layout(mock_genai, world_registry):
    """Test that the agent selects the correct location based on intent."""
    mock_client = mock_genai.Client.return_value
    
    # Mock Response
    mock_layout = SceneLayout(
        location_id="paris_studio",
        selected_objects=["blue_sofa"],
        scene_description="The Muse sits on the blue sofa in her Paris studio."
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_layout
    mock_client.models.generate_content.return_value = mock_response
    
    agent = ArchitectAgent()
    layout = agent.plan_scene_layout("She is relaxing in her studio", world_registry)
    
    assert layout.location_id == "paris_studio"
    assert "blue_sofa" in layout.selected_objects
    mock_client.models.generate_content.assert_called_once()
