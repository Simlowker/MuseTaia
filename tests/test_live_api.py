"""Tests for the LiveApiService."""

import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.services.live_api import LiveApiService

@pytest.fixture
def mock_genai():
    with patch("app.core.services.live_api.genai") as mock_gen:
        yield mock_gen

@pytest.mark.asyncio
async def test_live_session_connection(mock_genai):
    """Test that the live session connects correctly."""
    mock_client = mock_genai.Client.return_value
    
    # Mock the async context manager client.live.connect
    mock_session = AsyncMock()
    mock_connect = MagicMock()
    mock_connect.__aenter__.return_value = mock_session
    mock_client.live.connect.return_value = mock_connect
    
    service = LiveApiService()
    
    async with service.session() as session:
        assert session == mock_session
        mock_client.live.connect.assert_called_once()

@pytest.mark.asyncio
async def test_run_interaction_loop(mock_genai):
    """Test the interaction loop with a mock session."""
    mock_client = mock_genai.Client.return_value
    mock_session = AsyncMock()
    
    # Mock session.receive() as an async generator
    # Using MagicMock instead of AsyncMock for the method itself
    mock_session.receive = MagicMock()
    async def mock_receive():
        yield "msg1"
        yield "msg2"
    
    mock_session.receive.side_effect = mock_receive
    
    mock_connect = MagicMock()
    mock_connect.__aenter__.return_value = mock_session
    mock_client.live.connect.return_value = mock_connect
    
    service = LiveApiService()
    
    received_messages = []
    async def on_message(msg):
        received_messages.append(msg)
        
    await service.run_interaction_loop(on_message, initial_message="Hello")
    
    assert received_messages == ["msg1", "msg2"]
    mock_session.send.assert_called_once_with(input="Hello", end_of_turn=True)
