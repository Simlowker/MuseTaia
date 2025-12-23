"""Tests for Creative Studio Lobe (Narrative Architect & Visual Virtuoso)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.narrative_architect import NarrativeArchitect
from app.agents.visual_virtuoso import VisualVirtuoso
from app.agents.narrative_agent import ScriptOutput

@pytest.fixture
def mock_clients():
    with patch("google.genai.Client") as mock_genai, \
         patch("app.core.services.comfy_api.requests") as mock_requests:
        yield mock_genai, mock_requests

def test_narrative_architect_planning(mock_clients):
    architect = NarrativeArchitect()
    script = ScriptOutput(
        title="Sovereign Dawn",
        script="A new era begins...",
        caption="#sovereignty",
        estimated_duration=5
    )
    
    nodes = architect.plan_production_nodes(script)
    
    assert len(nodes) == 3
    assert nodes[0]["type"] == "visual_gen"
    assert nodes[2]["type"] == "motion_gen"

def test_visual_virtuoso_nodal_execution(mock_clients):
    mock_genai, mock_requests = mock_clients
    
    # Mock ComfyUI response
    mock_response = MagicMock()
    mock_response.json.return_value = {"prompt_id": "test-123"}
    mock_requests.post.return_value = mock_response
    
    virtuoso = VisualVirtuoso()
    nodes = [{"type": "visual_gen", "prompt": "test"}]
    
    prompt_id = virtuoso.generate_nodal_workflow(nodes)
    
    assert prompt_id == "test-123"
    assert mock_requests.post.called
