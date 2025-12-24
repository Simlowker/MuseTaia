"""Tests for the RootAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.root_agent import RootAgent
from app.agents.protocols.master_sync import MasterSource

@pytest.fixture
def mock_genai():
    with patch("app.agents.root_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_root_agent_initialization(mock_genai):
    """Tests that the RootAgent initializes correctly with the model."""
    mock_client = mock_genai
    mock_chat = mock_client.chats.create.return_value
    
    agent = RootAgent(model_name="gemini-3.0-flash-preview")
    
    # Check that a chat was created
    mock_client.chats.create.assert_called_once()
    assert agent.chat_session == mock_chat

def test_root_agent_ping(mock_genai):
    """Tests the basic ping functionality."""
    mock_chat = mock_genai.chats.create.return_value
    # Mock the response from the agent
    mock_response = MagicMock()
    mock_response.text = "Pong"
    mock_chat.send_message.return_value = mock_response
    
    agent = RootAgent()
    response = agent.ping()
    
    assert response == "Pong"
    mock_chat.send_message.assert_called_with("Ping")

def test_root_agent_sensory_reaction(mock_genai):
    """Test that RootAgent reacts to sensory input and updates state."""
    mock_chat = mock_genai.chats.create.return_value
    mock_response = MagicMock()
    mock_response.text = "I should look into that fashion trend."
    mock_chat.send_message.return_value = mock_response
    
    with patch("app.agents.root_agent.StateManager") as mock_sm:
        mock_manager = mock_sm.return_value
        from app.state.models import Mood
        mock_manager.get_mood.return_value = Mood()
        
        agent = RootAgent()
        reaction = agent.process_sensory_input("New digital couture on runway")
        
        assert reaction == "I should look into that fashion trend."
        mock_chat.send_message.assert_called()
        assert "New digital couture" in mock_chat.send_message.call_args.args[0]
        # Verify state update
        mock_manager.update_mood.assert_called_once()
        assert mock_manager.update_mood.call_args.args[0].current_thought == reaction

def test_root_agent_parse_and_route(mock_genai):
    """Tests that RootAgent parses and routes commands correctly."""
    agent = RootAgent()
    intent = agent.parse_and_route("create a fashion post")
    
    assert intent.action == "create_post"
    assert intent.source == MasterSource.HUMAN
    assert intent.parameters["topic"] == "fashion"

def test_root_agent_execute_intent(mock_genai):
    """Tests that RootAgent generates a TaskGraph for an intent."""
    agent = RootAgent()
    mock_intent = MagicMock()
    mock_intent.command = "produce_content"
    mock_intent.trend_type = "fashion"
    mock_intent.raw_intent = "Sample raw intent"
    
    task_graph = agent.execute_intent(mock_intent)
    
    assert len(task_graph.nodes) > 0
    assert task_graph.root_intent == mock_intent