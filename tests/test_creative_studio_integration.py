"""Tests for Creative Studio Lobe (Narrative Architect & Visual Virtuoso)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.narrative_architect import NarrativeArchitect
from app.agents.visual_virtuoso import VisualVirtuoso
from app.agents.narrative_agent import ScriptOutput, AttentionDynamics

@pytest.fixture
def mock_clients():
    with patch("app.agents.visual_agent.get_genai_client") as mock_get, \
         patch("app.core.services.comfy_api.requests") as mock_requests:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client, mock_requests

def test_narrative_architect_planning(mock_clients):
    architect = NarrativeArchitect()
    script = ScriptOutput(
        title="Sovereign Dawn",
        script="A new era begins...",
        caption="#sovereignty",
        estimated_duration=10,
        attention_dynamics=AttentionDynamics(
            hook_intensity=0.9,
            pattern_interrupts=["glitch"],
            tempo_curve=[0.5, 0.8]
        )
    )
    
    nodes = architect.plan_production_nodes(script)
    
    assert len(nodes) == 3
    assert nodes[0]["type"] == "visual_gen"
    assert nodes[2]["type"] == "motion_gen"

def test_visual_virtuoso_nodal_execution(mock_clients):
    mock_client, mock_requests = mock_clients
    
    # Mock ComfyUI response
    mock_response = MagicMock()
    mock_response.json.return_value = {"prompt_id": "test-123"}
    mock_requests.post.return_value = mock_response
    
    # Mock assets manager inside VisualAgent (VisualVirtuoso base)
    with patch("app.agents.visual_virtuoso.IdentityLockedWorkflow.build_workflow") as mock_build:
        mock_build.return_value = {}
        virtuoso = VisualVirtuoso()
        prompt_id = virtuoso.generate_identity_image(
            prompt="test",
            subject_id="muse-01"
        )
    
    assert prompt_id == "test-123"
    assert mock_requests.post.called
