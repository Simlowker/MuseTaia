"""Tests for the Narrative Agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.narrative_agent import NarrativeAgent, ScriptOutput, AttentionDynamics
from app.state.models import Mood

@pytest.fixture
def mock_genai():
    with patch("app.agents.narrative_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_generate_script(mock_genai):
    """Test that the agent generates a script correctly."""
    mock_client = mock_genai
    
    # Mock the structured response
    mock_output = ScriptOutput(
        title="Fashion Week Vlog",
        script="[Visual: Walking down street] VO: Today is the day...",
        caption="Paris vibes! #fashion",
        estimated_duration=15,
        attention_dynamics=AttentionDynamics(
            hook_intensity=0.9,
            pattern_interrupts=["glitch"],
            tempo_curve=[0.5, 0.8]
        )
    )
    
    mock_response = MagicMock()
    mock_response.parsed = mock_output
    mock_client.models.generate_content.return_value = mock_response
    
    agent = NarrativeAgent()
    mood = Mood(valence=0.8, current_thought="Excited about the show")
    
    result = agent.generate_content(topic="Paris Fashion Week", mood=mood)
    
    assert result.title == "Fashion Week Vlog"
    assert "Paris vibes" in result.caption
    assert result.estimated_duration == 15
    
    # Verify the call included mood info
    call_args = mock_client.models.generate_content.call_args
    prompt_text = call_args.kwargs["contents"][0].parts[0].text
    assert "Excited about the show" in prompt_text
    
    # Verify search tool integration
    assert call_args.kwargs["config"].tools is not None
    assert len(call_args.kwargs["config"].tools) == 1

def test_initialization(mock_genai):
    """Test agent initialization."""
    agent = NarrativeAgent(model_name="gemini-3.0-pro")
    assert agent.model_name == "gemini-3.0-pro"
