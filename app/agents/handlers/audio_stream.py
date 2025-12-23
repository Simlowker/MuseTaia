"""Handler for processing real-time audio streams and server messages."""

import logging
from typing import Optional, Dict, Any
from google.genai import types

logger = logging.getLogger(__name__)

class AudioStreamHandler:
    """Processes audio-related interactions from the Live API."""

    def __init__(self):
        pass

    def extract_transcript(self, message: Any) -> Optional[str]:
        """Extracts text transcript from a LiveServerContent message.

        Args:
            message: The message received from the Gemini Live server.

        Returns:
            Optional[str]: The transcript text if available.
        """
        # The message structure for Multimodal Live is complex.
        # It yields server_content which contains turns and parts.
        
        # Based on SDK types: types.LiveServerMessage -> server_content -> model_turn -> parts
        try:
            if hasattr(message, 'server_content') and message.server_content:
                turn = message.server_content.model_turn
                if turn and turn.parts:
                    # Collect all text parts
                    texts = [p.text for p in turn.parts if p.text]
                    if texts:
                        return " ".join(texts)
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            
        return None

    def prepare_audio_input(self, audio_data: bytes) -> types.LiveClientRealtimeInput:
        """Wraps raw audio bytes into the format required by the Live API.

        Args:
            audio_data: Raw PCM audio data (usually 16kHz, mono, 16-bit).

        Returns:
            LiveClientRealtimeInput: Formatted input for session.send.
        """
        return types.LiveClientRealtimeInput(
            media_chunks=[
                types.Blob(data=audio_data, mime_type="audio/pcm")
            ]
        )
