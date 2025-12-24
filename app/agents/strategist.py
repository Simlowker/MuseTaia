"""High-Level Planner (HLP) for decoupled intent orchestration."""

import logging
from typing import Optional, Dict, Any, List
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.state.db_access import StateManager
from app.core.vertex_init import get_genai_client

logger = logging.getLogger(__name__)

class StrategistAgent:
    """The 'Brain' of the swarm. 
    
    In the HLP/Worker dichotomy, this agent only handles:
    1. Narrative Strategy (Moral Graph alignment).
    2. Budget Allocation (USD/Credit limits).
    3. Delegation (Choosing which Workers to use).
    """

    def __init__(self, model_name: str = "gemini-3.0-pro"):
        self.client = get_genai_client()
        self.model_name = model_name
        self.state_manager = StateManager()

    def define_strategy(self, intent: str, dna: Any) -> Dict[str, Any]:
        """Alias for plan_mission for script compatibility."""
        return self.plan_mission(intent, dna)

    def plan_mission(self, intent: str, dna: Any) -> Dict[str, Any]:
        """Translates a raw intent into a high-level strategic plan."""
        g = dna.identity.moral_graph
        
        prompt = f"""
        You are the High-Level Planner (HLP) for the Muse.
        
        MUSE DNA:
        - Autonomy: {g.autonomy}
        - Sophistication: {g.sophistication}
        - Technophilia: {g.technophilia}
        
        USER INTENT: "{intent}"
        
        TASK:
        1. Parse intent into a 'Narrative Angle'.
        2. Allocate budget (0.1 to 5.0 USD).
        3. Determine required worker types (e.g. ['narrative', 'visual', 'audio']).
        
        Return a structured JSON plan.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        import json
        return json.loads(response.text)

    def evaluate_roi(self, vvs_score: float, actual_cost: float) -> bool:
        """Post-production audit: Was the compute investment worth it?"""
        # Simple heuristic: ROI = VVS / Cost
        return (vvs_score / actual_cost) > 50.0

    def evaluate_production_roi(self, vvs_score: float, actual_cost: float) -> bool:
        """Alias for evaluate_roi for script compatibility."""
        return self.evaluate_roi(vvs_score, actual_cost)