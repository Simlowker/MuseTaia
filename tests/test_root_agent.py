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
    mock_agent = mock_client.agents.create.return_value
    
    agent = RootAgent(model_name="gemini-3.0-flash")
    
    # Check that the GenAI client was initialized
    mock_genai.Client.assert_called_once()
    # Check that an agent was created
    mock_client.agents.create.assert_called_once()
    assert agent.agent_instance == mock_agent

def test_root_agent_ping(mock_genai):
    """Tests the basic ping functionality."""
    mock_agent = mock_genai.Client.return_value.agents.create.return_value
    # Mock the response from the agent
    mock_response = MagicMock()
    mock_response.text = "Pong"
    mock_agent.chat.return_value.send_message.return_value = mock_response
    
    agent = RootAgent()
    response = agent.ping()
    
    assert response == "Pong"
    mock_agent.chat.return_value.send_message.assert_called_with("Ping")
