"""RevenueOptimizer Agent for maximizing ROI and managing compute arbitration."""

import logging
import json
import os
from typing import List, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class RevenueOptimizer:
    """Agent that ensures each dollar spent on API/GPU generates positive ROI.    
    Arbitrates between high-fidelity (Veo) and low-cost (Flux) rendering
    based on predicted monetization.
    """

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.matrix_path = "app/matrix/monetization_matrix.json"

    def _load_matrix(self) -> Dict[str, Any]:
        if os.path.exists(self.matrix_path):
            with open(self.matrix_path, 'r') as f:
                return json.load(f)
        return {}

    def arbitrate_compute(self, niche: str, vvs_score: float) -> str:
        """Decides which rendering pipeline to use based on ROI potential."""
        matrix = self._load_matrix()
        cpm = matrix.get("cpm_by_niche", {}).get(niche, 10.0)
        
        # Logic: If CPM is high and VVS is high, use Premium (Veo)
        if cpm > 30.0 and vvs_score > 70.0:
            return "veo-3.1-premium"
        return "flux-1.0-optimized"

    def match_sponsorships(self, content_topic: str) -> List[str]:
        """Scans for potential brand alignment based on content themes."""
        matrix = self._load_matrix()
        leads = matrix.get("sponsorship_leads", [])
        
        prompt = f"""
        Content Topic: {content_topic}
        Potential Leads: {leads}
        
        Which of these brands would pay the highest CPM for this content?
        Return a prioritized list of 3.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        )
        
        return response.text.split("\n")[:3]
