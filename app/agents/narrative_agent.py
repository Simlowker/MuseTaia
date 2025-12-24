"""NarrativeAgent implementation with High-Fidelity Attention Dynamics."""

from typing import List, Optional, Dict, Any
import logging
import google.genai as genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings
from app.agents.prompts.narrative import NARRATIVE_SYSTEM_INSTRUCTION
from app.state.models import Mood
from app.core.vertex_init import get_genai_client
from app.agents.base_worker import BaseWorker, WorkerOutput

logger = logging.getLogger(__name__)

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

class NarrativeAgent(BaseWorker):
    """The Screenwriter agent responsible for high-fidelity narrative production."""

    def __init__(self, agent_id: str = "narrative_01", model_name: str = "gemini-3-pro-preview"):
        """Initializes the NarrativeAgent."""
        super().__init__(agent_id=agent_id, agent_type="narrative")
        self.client = get_genai_client()
        self.model_name = model_name
        self.search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

    async def execute_task(self, instruction: str, context: Dict[str, Any]) -> WorkerOutput:
        """HLP/Worker contract: Executes narrative generation."""
        logger.info(f"WORKER: NarrativeAgent {self.agent_id} executing task: {instruction}")
        
        mood = context.get("mood", Mood())
        try:
            result = self.generate_content(instruction, mood)
            return WorkerOutput(
                status="success",
                data=result.model_dump(),
                artifacts=[]
            )
        except Exception as e:
            logger.error(f"WORKER: NarrativeAgent failed: {e}")
            return WorkerOutput(status="failure", data={"error": str(e)})

    def generate_content(self, topic: str, mood: Mood) -> ScriptOutput:
        """Generates a high-fidelity script with attention dynamics logic."""
        
        prompt = f"""
        You are the Narrative Architect for the Muse.
        Topic: {topic}
        
        Current Mood:
        - Valence: {mood.valence} / Arousal: {mood.arousal}
        - Current Thought: {mood.current_thought}
        
        STRICT RETENTION RULES:
        1. Use Google Search to verify cultural authenticity.
        2. PATTERN INTERRUPTION: You MUST insert a drastic shift (camera angle, lighting change, glitch, or sound effect) at exactly [00:08], [00:16], [00:24], etc. Mark these moments with `attention_boost: true`.
        3. TEMPORAL TAGGING: Use tags like [00:00-00:02] for EVERY shot description to sync with Veo 3.1.
        4. DEFINITION: Populate the AttentionDynamics metadata with the specific timestamps and types of interrupts used.
        
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