"""RootAgent implementation using Google ADK / GenAI SDK."""

from typing import Optional, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.state.models import Mood
from app.state.db_access import StateManager

class RootAgent:
    """The central nervous system of the SMOS swarm."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
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
        self.state_manager = StateManager()

    def ping(self) -> str:
        """Sends a ping to the agent to verify connectivity.

        Returns:
            str: The agent's response.
        """
        response = self.chat_session.send_message("Ping")
        return response.text

    def process_sensory_input(self, stimulus: str) -> str:
        """Processes real-time sensory data and updates the Muse's internal thought state.

        Args:
            stimulus: A description of what the Muse just perceived (Vision/Audio).

        Returns:
            str: The updated internal thought or reaction.
        """
        
        prompt = f"""
        SENSORY INPUT: "{stimulus}"
        
        You just perceived this in real-time. 
        How does this affect your current thought process? 
        Briefly update your internal monologue (1-2 sentences).
        """
        
        response = self.chat_session.send_message(prompt)
        reaction = response.text.strip()
        
        # Update shared state
        current_mood = self.state_manager.get_mood()
        current_mood.current_thought = reaction
        self.state_manager.update_mood(current_mood)
        
        return reaction
