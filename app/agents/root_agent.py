"""RootAgent implementation using Google ADK / GenAI SDK."""

from typing import Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings

class RootAgent:
    """The central nervous system of the SMOS swarm."""

    def __init__(self, model_name: str = "gemini-3.0-flash"):
        """Initializes the RootAgent.

        Args:
            model_name: The name of the Gemini model to use.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.chat_session = self.client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction="You are the RootAgent of the Sovereign Muse OS."
            )
        )

    def ping(self) -> str:
        """Sends a ping to the agent to verify connectivity.

        Returns:
            str: The agent's response.
        """
        response = self.chat_session.send_message("Ping")
        return response.text
