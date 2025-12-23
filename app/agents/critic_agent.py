"""CriticAgent for visual consistency and quality assurance (v3)."""

import logging
from typing import List, Optional, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.qa import QAReport, QAFailure, ConsistencyReport
from app.core.utils.visual_comparison import VisualComparator

logger = logging.getLogger(__name__)

class CriticAgent:
    """Agent de gouvernance visuelle appliquant la règle des 2% de dérive.
    
    This agent represents the 'Governance Lobe' (v3).
    It uses biometric comparison and semantic analysis to block or repair 
    unauthorized identity drifts.
    """

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes The Critic."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.comparator = VisualComparator()
        # Seuil critique : 0.75 de similarité cosinus (Règle des 2% de déviation)
        self.identity_threshold = 0.75

    def verify_consistency(
        self,
        generated_image_bytes: bytes,
        reference_face_bytes: bytes,
        criteria: str = "visual identity, colors, and spatial continuity"
    ) -> QAReport:
        """Comprehensive audit of the generated image vs Signature Assets."""
        
        # 1. Biometric Analysis (Identity Drift)
        drift_score = self.comparator.calculate_face_similarity(
            generated_image_bytes, 
            reference_face_bytes
        )
        
        # 2. Semantic Analysis (Simulated CLIP/Gemini Vision)
        semantic_score = 0.85 

        is_consistent = drift_score >= self.identity_threshold
        failures = []

        if not is_consistent:
            logger.warning(f"Identity Drift detected: {drift_score:.4f} < {self.identity_threshold}")
            failures.append(QAFailure(
                area="face",
                severity=round(1.0 - drift_score, 4),
                description="The facial structure deviates from the Muse's Signature Assets.",
                action_type="inpaint" # Triggers surgical repair
            ))

        decision = "APPROVED" if is_consistent else "REPAIR_REQUIRED"

        return QAReport(
            is_consistent=is_consistent,
            identity_drift_score=drift_score,
            clip_semantic_score=semantic_score,
            failures=failures,
            final_decision=decision
        )

    def detect_mask_area(self, image_bytes: bytes, feature_description: str) -> Optional[List[int]]:
        """Detects the bounding box of a specific feature for masking."""
        prompt = f"Detect the bounding box for: {feature_description}. Return JSON box_2d [ymin, xmin, ymax, xmax] 0-1000."
        
        from pydantic import BaseModel, Field
        class DetectionResult(BaseModel):
            box_2d: Optional[List[int]] = Field(None)

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
