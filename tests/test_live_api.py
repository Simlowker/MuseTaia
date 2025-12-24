"""Tests for the LiveApiService."""

import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from google.genai import types
from app.core.services.live_api import LiveApiService

@pytest.fixture
def mock_genai():
    with patch("app.core.services.live_api.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

@pytest.mark.asyncio
async def test_live_session_connection(mock_genai):
    """Test that the live session connects correctly with context and voice."""
    mock_client = mock_genai
    
    # Mock the async context manager client.live.connect
    mock_session = AsyncMock()
    mock_connect = MagicMock()
    mock_connect.__aenter__.return_value = mock_session
    mock_client.live.connect.return_value = mock_connect
    
    with patch("app.core.services.live_api.SwarmToolbox"), \
         patch("app.core.services.live_api.ContextCacheManager"):
        
        service = LiveApiService()
        
        async with service.session() as session:
            assert session == mock_session
            mock_client.live.connect.assert_called_once()
            
            # Verify config
            call_args = mock_client.live.connect.call_args
            config = call_args.kwargs["config"]
            assert config.system_instruction is not None
            assert config.speech_config.voice_config.prebuilt_voice_config.voice_name == "Aoede"
            assert "AUDIO" in config.response_modalities

@pytest.mark.asyncio
async def test_run_interaction_loop_with_tool_call(mock_genai):
    """Test the interaction loop with a tool call."""
    mock_client = mock_genai
    mock_session = AsyncMock()
    
    # 1. Mock a tool call message
    mock_fc = MagicMock()
    mock_fc.name = "search_web"
    mock_fc.args = {"query": "cyberpunk"}
    mock_fc.id = "call_1"
    
    mock_msg_tool = MagicMock()
    mock_msg_tool.tool_call.function_calls = [mock_fc]
    mock_msg_tool.server_content = None
    
    mock_msg_text = MagicMock()
    mock_msg_text.tool_call = None
    
    async def mock_receive_iter():
        yield mock_msg_tool
        yield mock_msg_text
    
    # In the code: async for message in await session.receive()
    # So session.receive() must be an AsyncMock returning our generator
    mock_session.receive = AsyncMock(return_value=mock_receive_iter())
    
    mock_connect = MagicMock()
    mock_connect.__aenter__.return_value = mock_session
    mock_client.live.connect.return_value = mock_connect
    
    # Patch SwarmToolbox
    with patch("app.core.services.live_api.SwarmToolbox") as mock_toolbox_class:
        mock_toolbox = mock_toolbox_class.return_value
        mock_toolbox.execute_tool = AsyncMock(return_value={"result": "search result"})
        mock_toolbox.get_tool_definitions.return_value = []
        
        service = LiveApiService()
        
        received_messages = []
        async def on_message(msg):
            received_messages.append(msg)
            
        await service.run_interaction_loop(on_message, initial_message="Hello")
        
        assert len(received_messages) == 2
        # Verify tool was executed
        mock_toolbox.execute_tool.assert_called_once_with("search_web", {"query": "cyberpunk"})
        # Verify response was sent back to session
        mock_session.send_tool_response.assert_called_once()
        call_args = mock_session.send_tool_response.call_args
        responses = call_args.kwargs["function_responses"]
        assert responses[0].name == "search_web"
        assert responses[0].response == {"result": "search result"}

