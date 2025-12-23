"""Tests for the InteractiveRootAgent."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.interactive_root import InteractiveRootAgent
from app.state.models import Mood

@pytest.fixture
def mock_deps():
    with patch("app.agents.interactive_root.LiveApiService") as m_live, \
         patch("app.agents.interactive_root.StateManager") as m_state:
        yield {
            "live": m_live.return_value,
            "state": m_state.return_value
        }

@pytest.mark.asyncio
async def test_start_talk(mock_deps):
    agent = InteractiveRootAgent()
    mock_deps["live"].run_interaction_loop = AsyncMock()
    
    await agent.start_talk("Greetings")
    
    mock_deps["live"].run_interaction_loop.assert_called_once()
    call_args = mock_deps["live"].run_interaction_loop.call_args
    assert call_args.kwargs["initial_message"] == "Greetings"

@pytest.mark.asyncio
async def test_on_message_updates_state(mock_deps):
    agent = InteractiveRootAgent()
    mock_deps["state"].get_mood.return_value = Mood()
    
    # Mock message with text
    mock_msg = MagicMock()
    mock_part = MagicMock()
    mock_part.text = "I am thinking about art."
    mock_msg.server_content.model_turn.parts = [mock_part]
    
    await agent._on_message(mock_msg)
    
    mock_deps["state"].update_mood.assert_called_once()
    updated_mood = mock_deps["state"].update_mood.call_args.args[0]
    assert updated_mood.current_thought == "I am thinking about art."

