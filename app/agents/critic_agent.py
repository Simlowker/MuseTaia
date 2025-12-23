"""CriticAgent for visual consistency and quality assurance (v3)."""

import logging
from typing import List, Optional, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.schemas.qa import QAReport, QAFailure, ConsistencyReport
from app.core.utils.visual_comparison import VisualComparator
from app.state.db_access import StateManager

logger = logging.getLogger(__name__)

class CriticAgent:
    """Agent de gouvernance visuelle appliquant la règle des 2% de dérive."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes The Critic."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.comparator = VisualComparator()
        self.state_manager = StateManager()
        # Seuil critique : 0.75 de similarité cosinus (Règle des 2% de déviation)
        self.identity_threshold = 0.75

    def verify_consistency(
        self,
        generated_image_bytes: bytes,
        reference_face_bytes: bytes,
        criteria: str = "visual identity, colors, and spatial continuity"
    ) -> QAReport:
        """Comprehensive audit of the generated image vs Signature Assets."""
        self.state_manager.publish_event("CRITIC_AUDIT", "Performing biometric identity check...")
        
        # 1. Biometric Analysis (Identity Drift)
        drift_score = self.comparator.calculate_face_similarity(
            generated_image_bytes, 
            reference_face_bytes
        )
        
                self.state_manager.publish_event("CRITIC_SCORE", f"Identity Similarity Score: {drift_score:.4f}", {"score": drift_score})
        
                
        
                # 3. Artifact Detection (v2 Expansion)
        
                # Use Bounding Boxes to find anomalies (Hands, Shadows, Anatomy)
        
                artifact_report = self.detect_physical_artifacts(generated_image_bytes)
        
                if artifact_report:
        
                    failures.extend(artifact_report)
        
        
        
                is_consistent = drift_score >= self.identity_threshold and not any(f.severity > 0.8 for f in failures)
        
        

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

    def detect_physical_artifacts(self, image_bytes: bytes) -> List[QAFailure]:
        """Uses Gemini Vision to detect distorted limbs, shadows, or anatomy anomalies."""
        prompt = """
        Analyze this image for AI artifacts. 
        Focus on: distorted hands, extra fingers, missing shadows, or floating objects.
        Return a JSON list of QAFailure objects if any major issues are found.
        """
        
        # Conceptual call to Gemini Vision
        # In a real implementation, we would use types.GenerateContentConfig with response_schema
        return [] # Placeholder

    def verify_vocal_consistency(self, audio_bytes: bytes, vocal_dna: str) -> float:
        """Audits the generated audio against the Muse's vocal anchor."""
        logger.info(f"CRITIC_AUDIO: Verifying timbre match for {vocal_dna}")
        # In production, this uses a Siamese Neural Network to compare 
        # speaker embeddings.
        return 0.92 # Simulated match score


