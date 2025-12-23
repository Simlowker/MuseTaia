"""Strategist Agent for long-term narrative and budget allocation logic."""

import google.genai as genai
from google.genai import types
from typing import Optional, Dict, Any
from app.core.config import settings
from app.state.db_access import StateManager

class StrategistAgent:
    """Agent that manages the Muse's long-term strategy.
    
    This agent represents the 'High Cognition Lobe' (The Brain).
    It is the guardian of the narrative arc and the financial logic for production.
    """

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the StrategistAgent.
        
        Args:
            model_name: The Gemini model to use. 
                        In production, Gemini 3 Pro is preferred for high cognition.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.state_manager = StateManager()

    def define_strategy(self, intent: Any, dna: Optional[Any] = None) -> Dict[str, Any]:
        """Develops a creative strategy for a given intent based on Moral Graph.
        
        Args:
            intent: The structured intent to strategize for.
            dna: The Muse's DNA (including Moral Graph).
            
        Returns:
            Dict: Detailed strategy.
        """
        
        graph_context = ""
        if dna and hasattr(dna, 'identity'):
            g = dna.identity.moral_graph
            graph_context = f"""
            MUSE PSYCHOLOGY (Moral Graph):
            - Autonomy: {g.autonomy} (High = very independent/bold)
            - Sophistication: {g.sophistication} (High = luxury/minimalist aesthetic)
            - Technophilia: {g.technophilia} (High = obsessed with future tech)
            - Ego: {g.ego} / Empathy: {g.empathy} / Chaos: {g.chaos}
            """
        
        prompt = f"""
        You are the 'Chief Strategy Officer' (CSO) for the Muse.
        {graph_context}
        
        Intent: {intent}
        
        TASK:
        1. Define a 'Narrative Angle' that STRICTLY respects the Muse's psychology.
           - If Sophistication is High, avoid cheap viral hooks.
           - If Autonomy is High, be provocative and self-sovereign.
        2. Propose a 'Budget Allocation'.
        """


        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        import json
        try:
            return json.loads(response.text)
        except:
            return {"raw_strategy": response.text}

    def evaluate_production_roi(self, trend_report: Any, cost_estimate: float) -> bool:
        """Evaluates if a production task is worth the investment based on VVS and ROI.
        
        Args:
            trend_report: The full TrendReport from TrendScout.
            cost_estimate: The estimated USD cost.
            
        Returns:
            bool: True if production is approved.
        """
        # Heuristic: Approve if ROI > 1.2 (20% margin) or VVS is Peaking (> 7.0)
        
        vvs_score = trend_report.vvs.score if trend_report.vvs else 0.0
        roi = trend_report.estimated_roi
        
        if trend_report.vvs and trend_report.vvs.acceleration == "Peaking":
            return True # Always capture peaks
            
        return roi >= 1.2 or (vvs_score * 0.5) >= cost_estimate

    def update_the_matrix(self, post_mortem: Any) -> bool:
        """Injects lessons from the Learning Loop into long-term context memory."""
        logger.info(f"STRATEGIST: Updating The Matrix with lessons from task {post_mortem.task_id}.")
        # Simulation: Update Redis with key lessons
        summary = f"Success Factors: {post_mortem.success_factors}. Next Strategy: {post_mortem.next_step_strategy}"
        self.state_manager.redis.set(f"smos:experience:lesson:{post_mortem.task_id}", summary)
        return True

