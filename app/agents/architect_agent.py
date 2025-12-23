"ArchitectAgent for managing scene environments and spatial continuity."

import google.genai as genai
from google.genai import types
from typing import List
from app.core.config import settings
from app.matrix.world_dna import WorldRegistry
from app.core.schemas.world import SceneLayout
from app.core.vertex_init import get_genai_client

class ArchitectAgent:
    """The Space Guardian agent responsible for environmental consistency."""

    def __init__(self, model_name: str = "gemini-3.0-pro-preview"):
        """Initializes the ArchitectAgent.

        Args:
            model_name: The name of the Gemini model to use.
        """
        self.client = get_genai_client()
        self.model_name = model_name

    def plan_scene_layout(self, script_intent: str, world_registry: WorldRegistry) -> SceneLayout:
        """Selects the best location and objects for a given narrative intent.

        Args:
            script_intent: The narrative description or script part.
            world_registry: The registry containing all known locations and objects.

        Returns:
            SceneLayout: Structured environmental setup.
        """
        
        # 1. Prepare World Context
        locations_info = []
        for loc in world_registry.list_locations():
            context = world_registry.get_location_context(loc.location_id)
            locations_info.append(context)
        
        world_context = "\n\n".join(locations_info)

        # 2. Construct Prompt
        prompt = f"""
        You are the ArchitectAgent (Space Guardian). Your job is to maintain spatial continuity for a digital Muse.
        
        Given the following WORLD DNA (Available Locations and Objects):
        {world_context}
        
        And the following NARRATIVE INTENT:
        "{script_intent}"
        
        Choose the most appropriate location and recurring objects from the WORLD DNA.
        Maintain consistency. If the intent mentions a specific setting that matches a known location, use it.
        
        Output a JSON object matching the SceneLayout schema.
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
                response_mime_type="application/json",
                response_schema=SceneLayout
            )
        )

        return response.parsed
