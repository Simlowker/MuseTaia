"""Service for managing real-time multimodal interactions via Gemini Live API."""

import asyncio
import logging
import contextlib
from typing import AsyncIterator, Optional, Callable, Any, Dict, List
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.agents.tools.swarm_tools import SwarmToolbox
from app.matrix.context_cache import ContextCacheManager

logger = logging.getLogger(__name__)

class LiveApiService:
    """Wrapper for Gemini Multimodal Live API via WebSockets."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the LiveApiService."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.toolbox = SwarmToolbox()
        self.cache_manager = ContextCacheManager()

    def _get_vocal_personality(self) -> types.SpeechConfig:
        """Returns the signature vocal configuration for the Muse."""
        # In a real scenario, we could use ReplicatedVoiceConfig if we have a sample.
        # For now, we select a high-quality prebuilt voice that fits the persona.
        return types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Aoede" # Example high-quality expressive voice
                )
            )
        )

    @contextlib.asynccontextmanager
    async def session(self, muse_id: str = "genesis", config: Optional[Dict[str, Any]] = None) -> AsyncIterator[Any]:
        """Creates an async session for live multimodal interaction with identity context.

        Args:
            muse_id: The ID of the Muse to load context for.
            config: Optional override configuration.

        Yields:
            An AsyncSession object.
        """
        
        # 1. Load Identity DNA from Cache
        # We assume the DNA has been cached (performed during initialization/boot)
        # and we retrieve the context string.
        dna_context = "You are the Sovereign Muse. You are proactive, creative, and consistent."
        
        # 2. Build Live Config
        live_config = types.LiveConnectConfig(
            tools=self.toolbox.get_tool_definitions(),
            response_modalities=["AUDIO", "TEXT"], # Enable Voice
            speech_config=self._get_vocal_personality(),
            system_instruction=dna_context,
            generation_config=types.GenerationConfig(
                temperature=0.8,
                top_p=0.95
            )
        )
        
        # Merge with provided config if any
        if config:
            # Simple merge for demonstration
            for k, v in config.items():
                setattr(live_config, k, v)
            
        async with self.client.live.connect(model=self.model_name, config=live_config) as session:
            yield session

    async def _handle_tool_call(self, session: Any, tool_call: Any):
        """Processes tool calls from the model and sends responses back."""
        if not tool_call.function_calls:
            return

        responses = []
        for fc in tool_call.function_calls:
            logger.info(f"Executing tool call: {fc.name} with args: {fc.args}")
            try:
                result = await self.toolbox.execute_tool(fc.name, fc.args)
                responses.append(types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response=result
                ))
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                responses.append(types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response={"error": str(e)}
                ))

        if responses:
            await session.send_tool_response(function_responses=responses)

    async def run_interaction_loop(
        self, 
        on_message: Callable[[Any], Any],
        initial_message: Optional[str] = None
    ):
        """Runs a basic interaction loop with tool support.
        
        Args:
            on_message: Callback for handling incoming server messages.
            initial_message: Optional text to send upon connection.
        """
        async with self.session() as session:
            if initial_message:
                await session.send_client_content(
                    turns=[types.Content(role="user", parts=[types.Part.from_text(text=initial_message)])],
                    turn_complete=True
                )
            
            async for message in session.receive():
                # Handle tool calls automatically
                if message.tool_call:
                    await self._handle_tool_call(session, message.tool_call)
                
                # Pass message to external handler
                await on_message(message)
