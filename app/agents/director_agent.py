"""DirectorAgent implementation using Veo 3.1 via Google GenAI SDK."""

from typing import Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings

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
        duration_seconds: int = 5,
        resolution: str = "1080p"
    ) -> bytes:
        """Generates a video based on a prompt and optional reference image.

        Args:
            prompt: The text description of the motion and scene.
            image_bytes: Optional starting frame (Image-to-Video).
            duration_seconds: Target length of the clip.
            resolution: Output resolution (e.g., '1080p', '720p').

        Returns:
            bytes: The raw video data of the first generated video.
        """
        
        image = None
        if image_bytes:
            image = types.Image(image_bytes=image_bytes)

        # Veo 3.1 generation is a Long Running Operation (LRO)
        operation = self.client.models.generate_videos(
            model=self.model_name,
            prompt=prompt,
            image=image,
            config=types.GenerateVideosConfig(
                duration_seconds=duration_seconds,
                resolution=resolution,
                number_of_videos=1,
                person_generation="ALLOW_ADULT",
                enhance_prompt=True
            )
        )

        # Wait for completion (blocking for now in this MVP implementation)
        response = operation.result()
        
        # Return the bytes of the first video
        return response.generated_videos[0].video_bytes
