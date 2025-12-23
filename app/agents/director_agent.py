"""DirectorAgent implementation using Veo 3.1 via Google GenAI SDK."""

import logging
from typing import Optional, List, Tuple, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.screenplay import ShotType, CameraMovement

from app.core.vertex_init import get_genai_client

logger = logging.getLogger(__name__)

class DirectorAgent:
    """The Cinematographer agent responsible for generating video content."""

    def __init__(self, model_name: str = "veo-3.1"):
        """Initializes the DirectorAgent.

        Args:
            model_name: The name of the Veo model to use.
        """
        self.client = get_genai_client()
        self.model_name = model_name

    def generate_video(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        reference_images: Optional[List[Tuple[bytes, str]]] = None,
        duration_seconds: int = 5,
        resolution: str = "1080p",
        shot_type: ShotType = ShotType.MEDIUM,
        camera_movement: CameraMovement = CameraMovement.STATIC,
        temporal_segments: Optional[List[Dict[str, Any]]] = None
    ) -> bytes:
        """Generates a video with precise temporal orchestration."""
        
        # 1. Construct Base Cinematic Prompt
        cinematic_directives = f"Shot type: {shot_type.value}. Camera movement: {camera_movement.value}."
        
        # 2. Add Temporal Segments (v2 Feature)
        segment_directives = ""
        if temporal_segments:
            for seg in temporal_segments:
                segment_directives += f" [{seg['start']}-{seg['end']}]: {seg['action']}."
        
        full_prompt = f"{cinematic_directives} {segment_directives} {prompt}"

        
        image = None
        if image_bytes:
            image = types.Image(image_bytes=image_bytes)

        config_params = {
            "duration_seconds": duration_seconds,
            "resolution": resolution,
            "number_of_videos": 1,
            "person_generation": "ALLOW_ADULT",
            "enhance_prompt": True
        }

        if reference_images:
            config_params["reference_images"] = [
                types.VideoGenerationReferenceImage(
                    image=types.Image(image_bytes=img_bytes),
                    reference_type=ref_type
                ) for img_bytes, ref_type in reference_images
            ]

        # Veo 3.1 generation is a Long Running Operation (LRO)
        try:
            operation = self.client.models.generate_videos(
                model=self.model_name,
                prompt=full_prompt,
                image=image,
                config=types.GenerateVideosConfig(**config_params)
            )

            # Wait for completion (blocking for now in this MVP implementation)
            # Timeout set to 10 minutes (Veo can be slow)
            response = operation.result(timeout=600)
            
            if not response.generated_videos:
                raise RuntimeError("Veo 3.1 returned no videos.")

            # Return the bytes of the first video
            return response.generated_videos[0].video_bytes
        except Exception as e:
            logger.error(f"DIRECTOR: Video generation failed: {e}")
            raise
