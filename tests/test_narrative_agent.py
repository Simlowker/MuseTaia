"""Tests for the Narrative Agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.narrative_agent import NarrativeAgent, ScriptOutput
from app.state.models import Mood

@pytest.fixture
def mock_genai():
    with patch("app.agents.narrative_agent.genai") as mock_gen:
        yield mock_gen

def test_generate_script(mock_genai):
    """Test that the agent generates a script correctly."""
    mock_client = mock_genai.Client.return_value
    
    # Mock the structured response
    mock_output = ScriptOutput(
        title="Fashion Week Vlog",
        script="[Visual: Walking down street] VO: Today is the day...",
        caption="Paris vibes! #fashion",
        estimated_duration=15
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

def test_initialization(mock_genai):
    """Test agent initialization."""
    agent = NarrativeAgent(model_name="gemini-3.0-pro")
    mock_genai.Client.assert_called_once()
    assert agent.model_name == "gemini-3.0-pro"
