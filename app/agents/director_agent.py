"""DirectorAgent implementation using Veo 3.1 via Google GenAI SDK."""

import logging
from typing import Optional, List, Tuple, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.screenplay import ShotType, CameraMovement

from app.core.vertex_init import get_genai_client
from app.agents.base_worker import BaseWorker, WorkerOutput

logger = logging.getLogger(__name__)

class DirectorAgent(BaseWorker):
    """The Cinematographer agent responsible for generating video content."""

    def __init__(self, agent_id: str = "director_01", model_name: str = "veo-3.1"):
        """Initializes the DirectorAgent."""
        super().__init__(agent_id=agent_id, agent_type="director")
        self.client = get_genai_client()
        self.model_name = model_name

    async def execute_task(self, instruction: str, context: Dict[str, Any]) -> WorkerOutput:
        """HLP/Worker contract: Executes video generation."""
        logger.info(f"WORKER: DirectorAgent {self.agent_id} executing task: {instruction}")
        
        try:
            video_bytes = self.generate_video(
                prompt=instruction,
                image_bytes=context.get("image_bytes"),
                duration_seconds=context.get("duration", 5),
                shot_type=context.get("shot_type", ShotType.MEDIUM),
                camera_movement=context.get("camera_movement", CameraMovement.STATIC)
            )
            return WorkerOutput(
                status="success",
                data={},
                artifacts=[f"bytes://video_{self.agent_id}"]
            )
        except Exception as e:
            logger.error(f"WORKER: DirectorAgent failed: {e}")
            return WorkerOutput(status="failure", data={"error": str(e)})

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
        """Generates a video with precise temporal orchestration.
        
        This agent uses Meta-Prompting to sync visual actions with timestamps.
        Example: [00:00-00:02]: Dolly zoom on subject.
        """
        
        # 1. Base Cinematic Context
        cinematic_directives = f"Format: {resolution}. Style: Cinematic. Shot: {shot_type.value}. Movement: {camera_movement.value}."
        
        # 2. Meta-Prompting (Temporal Orchestration)
        segment_directives = ""
        if temporal_segments:
            for seg in temporal_segments:
                segment_directives += f" [{seg['start']}-{seg['end']}]: {seg['action']}."
        
        # If no segments provided but prompt contains tags, Veo 3.1 will handle them natively
        full_prompt = f"{cinematic_directives} {segment_directives} {prompt}"
        logger.info(f"DIRECTOR: Executing Meta-Prompt: {full_prompt[:100]}...")

        
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
