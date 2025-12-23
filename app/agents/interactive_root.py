"""Interactive RootAgent for managing real-time voice conversations."""

import logging
import asyncio
from typing import Optional, Any
from app.core.services.live_api import LiveApiService
from app.state.db_access import StateManager
from app.state.models import Mood

logger = logging.getLogger(__name__)

class InteractiveRootAgent:
    """The brain of the Muse during a live 'Sovereign Talk' session."""

    def __init__(self, muse_id: str = "genesis"):
        self.muse_id = muse_id
        self.live_service = LiveApiService()
        self.state_manager = StateManager()
        self.current_session = None

    async def _on_message(self, message: Any):
        """Callback for incoming messages from the Live API."""
        # 1. Process Text Transcripts (if any)
        # Transcripts help us update the internal thought state even if response is audio
        if hasattr(message, 'server_content') and message.server_content:
            turn = message.server_content.model_turn
            if turn and turn.parts:
                texts = [p.text for p in turn.parts if p.text]
                if texts:
                    combined_text = " ".join(texts)
                    logger.info(f"Muse said: {combined_text}")
                    
                    # Update state with latest thought
                    mood = self.state_manager.get_mood()
                    mood.current_thought = combined_text
                    self.state_manager.update_mood(mood)

        # 2. Handle Tool Calls
        # (Already handled internally by LiveApiService, but we can log here)
        if hasattr(message, 'tool_call') and message.tool_call:
            logger.info("Muse is performing a background action...")

    async def start_talk(self, initial_greeting: Optional[str] = "Hello, I am ready to talk."):
        """Starts the interactive voice session."""
        logger.info(f"Starting Sovereign Talk for {self.muse_id}...")
        
        # We use the interaction loop from live_service
        await self.live_service.run_interaction_loop(
            on_message=self._on_message,
            initial_message=initial_greeting
        )

    async def send_stimulus(self, text: str):
        """Sends an external stimulus (e.g. news alert) into the ongoing talk."""
        # This requires session persistence, which run_interaction_loop currently abstracts.
        # In a real implementation, we'd maintain the session object.
        pass
