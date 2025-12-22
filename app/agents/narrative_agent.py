"""NarrativeAgent implementation."""

import google.genai as genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings
from app.agents.prompts.narrative import NARRATIVE_SYSTEM_INSTRUCTION
from app.state.models import Mood

class ScriptOutput(BaseModel):
    """Structured output for a generated script."""
    title: str = Field(description="The title of the content piece")
    script: str = Field(description="The full script including visual and audio cues")
    caption: str = Field(description="Social media caption with hashtags")
    estimated_duration: int = Field(description="Estimated duration in seconds")

class NarrativeAgent:
    """The Screenwriter agent responsible for generating text-based content."""

    def __init__(self, model_name: str = "gemini-3.0-pro"):
        """Initializes the NarrativeAgent.

        Args:
            model_name: The name of the Gemini model to use.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    def generate_content(self, topic: str, mood: Mood) -> ScriptOutput:
        """Generates a script and caption based on a topic and current mood.

        Args:
            topic: The subject matter or intent.
            mood: The current emotional state of the Muse.

        Returns:
            ScriptOutput: The structured content.
        """
        
        prompt = f"""
        Topic: {topic}
        
        Current Mood:
        - Valence: {mood.valence}
        - Arousal: {mood.arousal}
        - Current Thought: {mood.current_thought}
        
        IMPORTANT: Use Google Search to verify any specific cultural references, dates, or slang terms to ensure authenticity and accuracy before writing the script.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=NARRATIVE_SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                response_schema=ScriptOutput,
                tools=[self.search_tool]
            )
        )

        return response.parsed
