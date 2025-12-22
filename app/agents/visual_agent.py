"""VisualAgent implementation using Imagen 3 via Google GenAI SDK."""

from typing import List, Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.matrix.assets_manager import SignatureAssetsManager

class VisualAgent:
    """The Photographer agent responsible for generating high-fidelity images."""

    def __init__(self, model_name: str = "imagen-3.0-generate-002"):
        """Initializes the VisualAgent.

        Args:
            model_name: The name of the Imagen 3 model to use.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.assets_manager = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)

    def generate_image(
        self,
        prompt: str,
        subject_id: Optional[str] = None,
        aspect_ratio: str = "1:1",
        number_of_images: int = 1
    ) -> bytes:
        """Generates an image based on a prompt and optional subject guidance.

        Args:
            prompt: The text description of the image.
            subject_id: The ID of the Muse to use for Subject Guidance.
            aspect_ratio: Aspect ratio (e.g., '1:1', '16:9').
            number_of_images: How many images to generate.

        Returns:
            bytes: The raw image data of the first generated image.
        """
        
        # Enhanced prompt for subject consistency if subject_id is provided
        enhanced_prompt = prompt
        if subject_id:
            # Fetch reference assets (Face, Profile, Style)
            # In a real scenario, we would use SubjectReferenceImage if supported by the SDK method.
            # For now, we fetch assets to ensure they exist and potentially use them.
            try:
                # We could potentially use these in an edit_image call or enhanced prompt
                self.assets_manager.download_asset(f"muses/{subject_id}/face.png")
                enhanced_prompt = f"Subject: {subject_id}. {prompt}"
            except Exception:
                pass # Fallback to original prompt if assets missing

        response = self.client.models.generate_images(
            model=self.model_name,
            prompt=enhanced_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=number_of_images,
                aspect_ratio=aspect_ratio,
                safety_filter_level="BLOCK_LOW_AND_ABOVE",
                person_generation="ALLOW_ADULT"
            )
        )

        # Return the bytes of the first image
        return response.generated_images[0].image_bytes
