"""VisualAgent implementation using Imagen 3 via Google GenAI SDK."""

from typing import List, Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.vertex_init import get_genai_client

class VisualAgent:
    """The Photographer agent responsible for generating high-fidelity images."""

    def __init__(self, model_name: str = "imagen-3.0-generate-002"):
        """Initializes the VisualAgent.

        Args:
            model_name: The name of the Imagen 3 model to use.
        """
        self.client = get_genai_client()
        self.model_name = model_name
        self.assets_manager = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)


    def generate_image(
        self,
        prompt: str,
        subject_id: Optional[str] = None,
        style_id: Optional[str] = None,
        location_id: Optional[str] = None,
        object_ids: Optional[List[str]] = None,
        item_ids: Optional[List[str]] = None,
        aspect_ratio: str = "1:1",
        number_of_images: int = 1
    ) -> bytes:
        """Generates an image based on a prompt and optional subject/style/world/wardrobe guidance.

        Args:
            prompt: The text description of the image.
            subject_id: The ID of the Muse to use for Subject Guidance.
            style_id: The ID of a style asset to use for Style Guidance.
            location_id: The ID of the persistent location.
            object_ids: List of IDs of persistent objects to include.
            item_ids: List of IDs of persistent wardrobe items.
            aspect_ratio: Aspect ratio (e.g., '1:1', '16:9').
            number_of_images: How many images to generate.

        Returns:
            bytes: The raw image data of the first generated image.
        """
        
        enhanced_prompt = prompt
        
        # 1. Subject Guidance
        if subject_id:
            try:
                self.assets_manager.download_asset(f"muses/{subject_id}/face.png")
                enhanced_prompt = f"Subject: {subject_id}. {enhanced_prompt}"
            except Exception:
                pass

        # 2. Style Guidance
        if style_id:
            try:
                self.assets_manager.download_asset(f"styles/{style_id}.png")
                enhanced_prompt += f" Style: {style_id}"
            except Exception:
                pass

        # 3. World Guidance (Locations & Objects)
        if location_id:
            try:
                self.assets_manager.download_asset(f"world/locations/{location_id}/reference.png")
                enhanced_prompt += f" Location: {location_id}"
            except Exception:
                pass
        
        if object_ids:
            for obj_id in object_ids:
                try:
                    self.assets_manager.download_asset(f"world/objects/{obj_id}/reference.png")
                    enhanced_prompt += f" Including Object: {obj_id}"
                except Exception:
                    pass

        # 4. Wardrobe Guidance
        if item_ids:
            for item_id in item_ids:
                try:
                    # Fetching from the appropriate path
                    self.assets_manager.download_asset(f"wardrobe/items/{item_id}/reference.png")
                    enhanced_prompt += f" Wearing: {item_id}"
                except Exception:
                    pass

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

    def edit_image(
        self,
        prompt: str,
        base_image_bytes: bytes,
        mask_image_bytes: Optional[bytes] = None,
        number_of_images: int = 1
    ) -> bytes:
        """Edits an image using mask-based inpainting.

        Args:
            prompt: Text description of the desired edit.
            base_image_bytes: The original image to edit.
            mask_image_bytes: The binary mask (white = edit area, black = preserve).
            number_of_images: Number of images to generate.

        Returns:
            bytes: The edited image data.
        """
        
        reference_images = [
            types.RawReferenceImage(
                reference_id=1,
                reference_image=types.Image(image_bytes=base_image_bytes)
            )
        ]
        
        if mask_image_bytes:
            reference_images.append(
                types.MaskReferenceImage(
                    reference_id=2,
                    reference_image=types.Image(image_bytes=mask_image_bytes),
                    config=types.MaskReferenceConfig(mask_mode="MASK_MODE_USER_PROVIDED")
                )
            )
            
        response = self.client.models.edit_image(
            model=self.model_name,
            prompt=prompt,
            reference_images=reference_images,
            config=types.EditImageConfig(
                number_of_images=number_of_images,
                safety_filter_level="BLOCK_LOW_AND_ABOVE",
                person_generation="ALLOW_ADULT"
            )
        )
        
        return response.generated_images[0].image_bytes
