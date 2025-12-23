"""Service for managing real-time multimodal interactions via Gemini Live API."""

import asyncio
import logging
import contextlib
from typing import AsyncIterator, Optional, Callable, Any, Dict
import google.genai as genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class LiveApiService:
    """Wrapper for Gemini Multimodal Live API via WebSockets."""

    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """Initializes the LiveApiService.
        
        Note: Using gemini-2.0-flash-exp or similar as Multimodal Live 
        is often available in these preview versions.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    @contextlib.asynccontextmanager
    async def session(self, config: Optional[Dict[str, Any]] = None) -> AsyncIterator[Any]:
        """Creates an async session for live multimodal interaction.

        Args:
            config: Optional configuration for the live session.

        Yields:
            An AsyncSession object.
        """
        async with self.client.live.connect(model=self.model_name, config=config) as session:
            yield session

    async def run_interaction_loop(
        self, 
        on_message: Callable[[Any], Any],
        initial_message: Optional[str] = None
    ):
        """Runs a basic interaction loop.
        
        Args:
            on_message: Callback for handling incoming server messages.
            initial_message: Optional text to send upon connection.
        """
        async with self.session() as session:
            if initial_message:
                await session.send(input=initial_message, end_of_turn=True)
            
            async for message in session.receive():
                await on_message(message)
