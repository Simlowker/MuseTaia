"""Integration tests for NarrativeAgent using real Vertex AI."""

import pytest
from app.agents.narrative_agent import NarrativeAgent, ScriptOutput
from app.state.models import Mood

@pytest.mark.integration
@pytest.mark.slow
def test_narrative_generates_real_script(real_genai):
    """Teste la génération réelle d'un script via Gemini."""
    agent = NarrativeAgent()
    mood = Mood(valence=0.8, arousal=0.6, current_thought="Ready for fashion week")
    
    # Simple topic to save tokens
    result = agent.generate_content("Short teaser for a digital fashion show", mood)
    
    assert isinstance(result, ScriptOutput)
    assert len(result.title) > 0
    assert "[00:00]" in result.script or "[" in result.script
    assert result.attention_dynamics is not None
    assert result.estimated_duration > 0