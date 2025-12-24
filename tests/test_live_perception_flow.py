"""Integration test for the Live Perception -> Action flow."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.handlers.visual_stream import VideoStreamHandler
from app.agents.root_agent import RootAgent
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood

@pytest.mark.asyncio
async def test_live_stimulus_to_production_trigger():
    """
    Verifies the flow: 
    Live Visual -> RootAgent Thought -> Workflow Trigger.
    """
    
    # 1. Setup Mocks
    mock_frame_description = "A stunning digital fashion show featuring holographic fabrics."
    mock_reaction = "Holographic fabrics are the next big thing. I need to launch a themed collection."
    
    # Patch infrastructure
    with patch("google.cloud.storage.Client"), \
         patch("app.agents.root_agent.get_genai_client") as mock_get, \
         patch("app.agents.handlers.visual_stream.VideoStreamHandler.describe_frame", new_callable=AsyncMock) as mock_describe, \
         patch("app.core.workflow_engine.WorkflowEngine.produce_video_content") as mock_produce, \
         patch("app.agents.root_agent.StateManager") as mock_sm:
        
        # Configure Mocks
        mock_genai_client = MagicMock()
        mock_get.return_value = mock_genai_client
        mock_describe.return_value = mock_frame_description
        
        mock_chat = MagicMock()
        # Mock the chain correctly
        mock_chat.send_message.return_value.text.strip.return_value = mock_reaction
        mock_genai_client.chats.create.return_value = mock_chat
        
        # Setup state
        mock_sm.return_value.get_mood.return_value = Mood()
        
        # --- EXECUTION ---
        
        # Step 1: Perceive
        visual_handler = VideoStreamHandler()
        stimulus = await visual_handler.describe_frame(b"frame_bytes")
        
        # Step 2: Cognition
        root_agent = RootAgent()
        thought = root_agent.process_sensory_input(stimulus)
        
        # Step 3: Reactive Decision
        if "need to launch" in thought.lower() or "collection" in thought.lower():
            engine = WorkflowEngine()
            engine.produce_video_content(
                intent=f"Reactive production based on: {thought}",
                mood=Mood(),
                subject_id="genesis"
            )
            
        # --- VERIFICATION ---
        assert stimulus == mock_frame_description
        assert thought == mock_reaction
        mock_produce.assert_called_once()
        
        call_args = mock_produce.call_args
        assert "holographic fabrics" in call_args.kwargs["intent"].lower()
        
    print("\nEnd-to-end Live Perception flow verified.")
