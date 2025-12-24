"""Integration test for the Sovereign Talk (Voice-to-Action) flow."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.interactive_root import InteractiveRootAgent
from app.core.services.live_api import LiveApiService
from app.agents.tools.swarm_tools import SwarmToolbox
from google.genai import types

@pytest.mark.asyncio
async def test_voice_to_tool_execution_flow():
    """
    Verifies the full loop:
    1. User speaks (Simulated).
    2. Live API receives intent and issues Tool Call.
    3. LiveApiService dispatches tool to SwarmToolbox.
    4. SwarmToolbox executes underlying Agent (Visual).
    5. Result is returned to Live API session.
    """
    
    # 1. Setup Mocks
    mock_visual_output = {"status": "success", "message": "Image generated."}
    
    with patch("app.core.services.live_api.get_genai_client") as mock_get, \
         patch("app.core.services.live_api.SwarmToolbox") as mock_toolbox_class, \
         patch("app.agents.interactive_root.StateManager"):
        
        mock_genai_client = MagicMock()
        mock_get.return_value = mock_genai_client
        
        # Configure Toolbox
        mock_toolbox = mock_toolbox_class.return_value
        mock_toolbox.execute_tool = AsyncMock(return_value=mock_visual_output)
        mock_toolbox.get_tool_definitions.return_value = [MagicMock()]
        
        # Configure Live Session
        mock_session = AsyncMock()
        
        # Simulate sequence of messages from server
        # First: A tool call to generate visual
        mock_fc = MagicMock()
        mock_fc.name = "generate_visual_asset"
        mock_fc.args = {"prompt": "Cyberpunk Muse"}
        mock_fc.id = "call_123"
        
        mock_msg_tool_call = MagicMock()
        mock_msg_tool_call.tool_call.function_calls = [mock_fc]
        mock_msg_tool_call.server_content = None
        
        # Second: A textual confirmation from the model
        mock_msg_confirm = MagicMock()
        mock_msg_confirm.tool_call = None
        mock_part = MagicMock()
        mock_part.text = "I've started generating that cyberpunk asset for you."
        mock_msg_confirm.server_content.model_turn.parts = [mock_part]
        
        async def mock_receive_iter():
            yield mock_msg_tool_call
            yield mock_msg_confirm
            
        mock_session.receive = AsyncMock(return_value=mock_receive_iter())
        
        # Connect session
        mock_connect = MagicMock()
        mock_connect.__aenter__ = AsyncMock(return_value=mock_session)
        mock_connect.__aexit__ = AsyncMock()
        mock_genai_client.live.connect.return_value = mock_connect
        
        # --- EXECUTION ---
        interactive_brain = InteractiveRootAgent()
        
        # Start the "Talk"
        # This will run the interaction loop, process the tool call, and then the confirmation
        await interactive_brain.start_talk(initial_greeting="I am listening.")
        
        # --- VERIFICATION ---
        
        # Verify Tool Dispatching
        mock_toolbox.execute_tool.assert_called_once_with(
            "generate_visual_asset", 
            {"prompt": "Cyberpunk Muse"}
        )
        
        # Verify Tool Response sent back to Gemini
        mock_session.send_tool_response.assert_called_once()
        sent_response = mock_session.send_tool_response.call_args.kwargs["function_responses"][0]
        assert sent_response.name == "generate_visual_asset"
        assert sent_response.response == mock_visual_output
        
        # Verify State was updated with the model's confirmation text
        # (Handled by InteractiveRootAgent._on_message)
        from app.state.models import Mood
        # StateManager was patched, check its update_mood call
        mock_sm = interactive_brain.state_manager
        mock_sm.update_mood.assert_called()
        last_mood = mock_sm.update_mood.call_args.args[0]
        assert "cyberpunk asset" in last_mood.current_thought
        
    print("\nEnd-to-end Voice Studio interaction verified.")
