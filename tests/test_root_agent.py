"""Tests for the RootAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.root_agent import RootAgent

@pytest.fixture
def mock_genai():
    # Patch the google.genai or ADK components
    # Assuming RootAgent uses 'google.genai' for this implementation based on the task desc
    with patch("app.agents.root_agent.genai") as mock_gen:
        yield mock_gen

def test_root_agent_initialization(mock_genai):
    """Tests that the RootAgent initializes correctly with the model."""
    mock_client = mock_genai.Client.return_value
    mock_chat = mock_client.chats.create.return_value
    
    agent = RootAgent(model_name="gemini-3.0-flash")
    
    # Check that the GenAI client was initialized
    mock_genai.Client.assert_called_once()
    # Check that a chat was created
    mock_client.chats.create.assert_called_once()
    assert agent.chat_session == mock_chat

def test_root_agent_ping(mock_genai):
    """Tests the basic ping functionality."""
    mock_chat = mock_genai.Client.return_value.chats.create.return_value
    # Mock the response from the agent
    mock_response = MagicMock()
    mock_response.text = "Pong"
    mock_chat.send_message.return_value = mock_response
    
    agent = RootAgent()
    response = agent.ping()
    
    assert response == "Pong"
    mock_chat.send_message.assert_called_with("Ping")
