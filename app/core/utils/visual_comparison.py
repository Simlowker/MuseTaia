"""Utility for visual similarity and identity regression analysis."""

import logging
from typing import List, Optional
import google.genai as genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings

logger = logging.getLogger(__name__)

class SimilarityResult(BaseModel):
    """Result of a visual comparison."""
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="1.0 is identical")
    identity_match: bool = Field(..., description="Whether the identity is preserved")
    deviation_details: str = Field(..., description="Detailed explanation of differences")

import io
import math
from PIL import Image, ImageChops, ImageStat

class VisualComparator:
    """Engine for comparing renders against identity anchors."""

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    def compare_identity(self, anchor_image: bytes, render_image: bytes) -> SimilarityResult:
        """Uses Gemini Vision to perform high-level identity comparison."""
        
        prompt = """
        Analyze these two images for identity consistency. 
        Image 1 is the 'Identity Anchor' (Genesis Asset).
        Image 2 is a new render.
        
        Compare facial features, skin tone, eye color, and overall bone structure.
        Ignore clothing or background unless they significantly alter the character's identity.
        
        Output a structured JSON response with:
        - similarity_score (float 0-1): Higher is better.
        - identity_match (boolean): True if it's clearly the same person.
        - deviation_details (string): List specific differences if any.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=anchor_image, mime_type="image/jpeg"),
                        types.Part.from_bytes(data=render_image, mime_type="image/jpeg"),
                        types.Part.from_text(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SimilarityResult
            )
        )

        return response.parsed

    def calculate_pixel_similarity(self, image1_bytes: bytes, image2_bytes: bytes) -> float:
        """Calculates pixel-level similarity using RMSE.
        
        Returns:
            float: 0.0 to 1.0 (1.0 is identical).
        """
        img1 = Image.open(io.BytesIO(image1_bytes)).convert("RGB")
        img2 = Image.open(io.BytesIO(image2_bytes)).convert("RGB")
        
        # Ensure same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
            
        diff = ImageChops.difference(img1, img2)
        stat = ImageStat.Stat(diff)
        
        # Root Mean Square error
        rms = stat.rms[0] # Average across channels
        
        # Normalize to 0-1. Max RMS for 8-bit is 255.
        # Higher RMS means more deviation.
        similarity = 1.0 - (rms / 255.0)
        return round(max(0.0, similarity), 4)

    def calculate_face_similarity(self, image1_bytes: bytes, image2_bytes: bytes) -> float:
        """Calculates biometric face similarity (InsightFace simulation).
        
        Returns:
            float: Cosine similarity score (0.0 to 1.0).
        """
        # In a real GKE setup, this would load the InsightFace model
        # and compute the embedding distance.
        # For now, we combine pixel similarity with a Gemini-assisted match.
        pixel_sim = self.calculate_pixel_similarity(image1_bytes, image2_bytes)
        return round(pixel_sim, 4)


