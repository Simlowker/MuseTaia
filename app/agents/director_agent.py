"""DirectorAgent implementation using Veo 3.1 via Google GenAI SDK."""

from typing import Optional, List, Tuple
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.screenplay import ShotType, CameraMovement

class DirectorAgent:
    """The Cinematographer agent responsible for generating video content."""

    def __init__(self, model_name: str = "veo-3.1"):
        """Initializes the DirectorAgent.

        Args:
            model_name: The name of the Veo model to use.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    def generate_video(
        self,
        prompt: str,
        image_bytes: Optional[bytes] = None,
        reference_images: Optional[List[Tuple[bytes, str]]] = None,
        duration_seconds: int = 5,
        resolution: str = "1080p",
        shot_type: ShotType = ShotType.MEDIUM,
        camera_movement: CameraMovement = CameraMovement.STATIC
    ) -> bytes:
        """Generates a video based on a prompt and optional reference images.

        Args:
            prompt: The text description of the motion and scene.
            image_bytes: Optional starting frame (Image-to-Video).
            reference_images: Optional list of (image_bytes, reference_type) tuples.
                             Types are usually 'ASSET' or 'STYLE'.
            duration_seconds: Target length of the clip.
            resolution: Output resolution (e.g., '1080p', '720p').
            shot_type: Standard cinematographic shot type.
            camera_movement: Camera movement type.

        Returns:
            bytes: The raw video data of the first generated video.
        """
        
        # Construct cinematic prompt
        cinematic_directives = f"Shot type: {shot_type.value}. Camera movement: {camera_movement.value}."
        full_prompt = f"{cinematic_directives} {prompt}"
        
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
        operation = self.client.models.generate_videos(
            model=self.model_name,
            prompt=full_prompt,
            image=image,
            config=types.GenerateVideosConfig(**config_params)
        )

        # Wait for completion (blocking for now in this MVP implementation)
        response = operation.result()
        
        # Return the bytes of the first video
        return response.generated_videos[0].video_bytes
