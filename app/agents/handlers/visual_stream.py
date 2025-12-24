"""Handler for processing real-time video streams and extracting visual context."""

import logging
from typing import Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.vertex_init import get_genai_client

logger = logging.getLogger(__name__)

class VideoStreamHandler:
    """Processes video frames to provide real-time visual perception for the Muse."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the VideoStreamHandler.

        Args:
            model_name: The Gemini model to use for visual analysis.
        """
        self.client = get_genai_client()
        self.model_name = model_name

    async def describe_frame(self, frame_bytes: bytes, prompt: str = "Describe the main visual elements in this frame concisely.") -> str:
        """Analyzes a single video frame and returns a textual description.

        Args:
            frame_bytes: Raw bytes of the video frame (e.g., JPEG/PNG).
            prompt: Instructions for the model.

        Returns:
            str: A concise visual description.
        """
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_bytes(data=frame_bytes, mime_type="image/jpeg"),
                            types.Part.from_text(text=prompt)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    top_p=0.9
                )
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error describing frame: {e}")
            return "Visual processing error."

    def summarize_stream_window(self, frame_descriptions: list[str]) -> str:
        """Summarizes a sequence of frame descriptions into a coherent narrative.

        Args:
            frame_descriptions: List of descriptions from recent frames.

        Returns:
            str: A summary of the visual event.
        """
        # This can be a simple join or a call to Gemini to synthesize movement
        if not frame_descriptions:
            return "No visual input."
            
        combined = " | ".join(frame_descriptions)
        # For MVP, we'll just return the combined string or a simple synthesis
        return f"Recent activity: {combined}"
