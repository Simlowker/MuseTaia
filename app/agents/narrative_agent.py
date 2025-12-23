"""NarrativeAgent implementation with High-Fidelity Attention Dynamics."""

from typing import List, Optional
import google.genai as genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings
from app.agents.prompts.narrative import NARRATIVE_SYSTEM_INSTRUCTION
from app.state.models import Mood

class AttentionDynamics(BaseModel):
    """Dynamic markers to maintain viewer retention."""
    hook_intensity: float = Field(..., ge=0.0, le=1.0, description="Strength of the initial 3 seconds")
    pattern_interrupts: List[str] = Field(..., description="Visual/Audio shifts triggered every 8 seconds")
    tempo_curve: List[float] = Field(..., description="Wavelength of energy throughout the script")

class ScriptOutput(BaseModel):
    """High-Fidelity structured output for a generated script."""
    title: str = Field(description="The title of the content piece")
    script: str = Field(description="Full script with [00:00] temporal tags and [VISUAL/AUDIO] cues")
    caption: str = Field(description="Social media caption with conversion-optimized hashtags")
    estimated_duration: int = Field(description="Estimated duration in seconds")
    attention_dynamics: AttentionDynamics = Field(description="Retention-focused technical metadata")

class NarrativeAgent:
    """The Screenwriter agent responsible for high-fidelity narrative production."""

    def __init__(self, model_name: str = "gemini-3.0-pro"):
        """Initializes the NarrativeAgent."""
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
        """Generates a high-fidelity script with attention dynamics logic."""
        
        prompt = f"""
        You are the Narrative Architect for the Muse.
        Topic: {topic}
        
        Current Mood:
        - Valence: {mood.valence} / Arousal: {mood.arousal}
        - Current Thought: {mood.current_thought}
        
        TASK:
        1. Use Google Search to verify cultural authenticity.
        2. Implement 'Pattern Interruption': Force a drastic shift in tone or visual every 8 seconds.
        3. Use temporal tags [00:00] throughout the script for precise Veo 3.1 synchronization.
        4. Define the AttentionDynamics metadata for the Forge.
        
        Return a high-fidelity ScriptOutput JSON.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
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