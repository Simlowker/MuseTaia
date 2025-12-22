"""RootAgent implementation using Google ADK / GenAI SDK."""

from typing import Optional
import google.genai as genai
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
        self.agent_instance = self.client.agents.create(
            model=model_name,
            instruction="You are the RootAgent of the Sovereign Muse OS."
        )

    def ping(self) -> str:
        """Sends a ping to the agent to verify connectivity.

        Returns:
            str: The agent's response.
        """
        chat = self.agent_instance.chat()
        response = chat.send_message("Ping")
        return response.text
