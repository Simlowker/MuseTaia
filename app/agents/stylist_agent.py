"""StylistAgent for managing the Muse's look and visual continuity."""

import google.genai as genai
from google.genai import types
from typing import List, Optional
from app.core.config import settings
from app.matrix.wardrobe_dna import WardrobeRegistry
from app.core.schemas.look import LookSelection
from app.core.schemas.world import SceneLayout
from app.state.models import Mood
from app.core.vertex_init import get_genai_client

class StylistAgent:
    """The Guardian of Look agent responsible for wardrobe and props."""

    def __init__(self, model_name: str = "gemini-3.0-pro-preview"):
        self.client = get_genai_client()
        self.model_name = model_name

    def select_look(
        self, 
        script_intent: str, 
        layout: SceneLayout, 
        mood: Mood, 
        registry: WardrobeRegistry
    ) -> LookSelection:
        """Selects the best outfit and props for a scene.

        Args:
            script_intent: The narrative description.
            layout: The planned spatial setup.
            mood: Current emotional state.
            registry: Registry of available wardrobe and props.

        Returns:
            LookSelection: Structured look configuration.
        """
        
        # 1. Prepare Wardrobe Context
        items_info = []
        for item in registry.items.values():
            items_info.append(f"- {item.item_id}: {item.name} ({', '.join(item.tags)}). {item.description}")
        
        props_info = []
        for prop in registry.props.values():
            props_info.append(f"- {prop.prop_id}: {prop.name}. {prop.description}")
            
        wardrobe_context = "AVAILABLE ITEMS:\n" + "\n".join(items_info) + "\n\nAVAILABLE PROPS:\n" + "\n".join(props_info)

        # 2. Construct Prompt
        prompt = f"""
        You are the StylistAgent (Guardian of Look). Your job is to maintain visual consistency and aesthetic excellence.
        
        {wardrobe_context}
        
        SCENE CONTEXT:
        Narrative: "{script_intent}"
        Location: {layout.location_id}
        Mood: Valence={mood.valence}, Arousal={mood.arousal}
        
        Task:
        Choose the most appropriate outfit (item_ids) and props (prop_ids) from the list above.
        Ensure the look matches the location's vibe and the Muse's emotional state.
        
        Output a JSON object matching the LookSelection schema.
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
                response_schema=LookSelection
            )
        )

        return response.parsed
