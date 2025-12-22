"""CriticAgent for visual consistency and quality assurance."""

from typing import List, Optional
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.qa import ConsistencyReport

class CriticAgent:
    """The 'Critic' agent responsible for maintaining visual and brand identity."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes The Critic.

        Args:
            model_name: The name of the Gemini model to use for vision tasks.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    def verify_consistency(
        self,
        reference_image_bytes: bytes,
        target_image_bytes: bytes,
        criteria: str = "visual identity, colors, and character features"
    ) -> ConsistencyReport:
        """Compares a target image against a reference image for consistency.

        Args:
            reference_image_bytes: The original 'Signature Asset' image.
            target_image_bytes: The newly generated image to verify.
            criteria: Specific aspects to focus on during verification.

        Returns:
            ConsistencyReport: Detailed analysis of the consistency.
        """
        
        prompt = f"""
        Analyze the two provided images for visual consistency based on the following criteria: {criteria}.
        
        Image 1 is the reference (Signature Asset).
        Image 2 is the generated content.
        
        Your goal is to perform a surgical QA check.
        
        Output a structured JSON response with:
        - is_consistent (boolean): True if deviations are minor/acceptable.
        - score (float 0-1): 1.0 is perfect match.
        - issues (list of strings): Summary of problems.
        - feedback (list of objects):
            - category: 'lighting', 'identity', 'anatomy', 'style'
            - description: Detailed issue description.
            - severity: 0.0 to 1.0
            - action_type: 'regenerate', 'inpaint', or 'none' if ok.
            - target_area: e.g. 'face', 'left hand', 'background'.
        - recommendations (string): High level advice.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=reference_image_bytes, mime_type="image/jpeg"),
                        types.Part.from_bytes(data=target_image_bytes, mime_type="image/jpeg"),
                        types.Part.from_text(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ConsistencyReport
            )
        )

        # Parse the structured response
        return response.parsed

    def detect_mask_area(self, image_bytes: bytes, feature_description: str) -> Optional[List[int]]:
        """Detects the bounding box of a specific feature for masking.

        Args:
            image_bytes: The image to analyze.
            feature_description: What to look for (e.g., "face", "shoes").

        Returns:
            List[int]: [ymin, xmin, ymax, xmax] coordinates (0-1000) or None if not found.
        """
        
        prompt = f"""
        Detect the bounding box for the following feature: {feature_description}.
        Return the box in [ymin, xmin, ymax, xmax] format normalized to 0-1000.
        If the feature is not found, return null.
        """
        
        # We define a minimal schema just for detection
        from pydantic import BaseModel, Field
        class DetectionResult(BaseModel):
            box_2d: Optional[List[int]] = Field(None, description="Bounding box")

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        types.Part.from_text(text=prompt)
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DetectionResult
            )
        )
        
        return response.parsed.box_2d
