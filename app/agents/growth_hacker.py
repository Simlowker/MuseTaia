"""GrowthHacker Agent for maximizing attention and analyzing retention."""

import logging
import yaml
import os
from typing import List, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)

class GrowthHacker:
    """Agent that transforms compute budget into maximum attention (Views/Likes).
    
    This agent manages 'attention_patterns.yaml' and optimizes hooks
    based on real-world performance audits.
    """

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.patterns_path = "app/matrix/attention_patterns.yaml"

    def _load_patterns(self) -> Dict[str, Any]:
        if os.path.exists(self.patterns_path):
            with open(self.patterns_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {}

    def analyze_performance(self, post_id: str, metrics: Dict[str, Any]) -> str:
        """Analyzes why a post succeeded or failed and synthesizes lessons."""
        patterns = self._load_patterns()
        
        prompt = f"""
        You are the 'Growth Hacker' for the Muse.
        
        Post ID: {post_id}
        Real Metrics: {metrics}
        Existing Knowledge (Patterns): {patterns}
        
        TASK:
        1. Compare performance against the average.
        2. Identify if the 'Hook' or 'Visual Style' was the primary driver.
        3. Propose a rule update for 'attention_patterns.yaml'.
        
        Return a technical 'Post-Mortem' analysis.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        )
        
        return response.text

    def generate_hooks(self, topic: str, count: int = 3) -> List[str]:
        """Proposes high-CTR hooks based on past successes."""
        patterns = self._load_patterns()
        best_hooks = sorted(patterns.get("high_performing_hooks", []), key=lambda x: x.get("retention_score", 0), reverse=True)
        
        prompt = f"""
        Generate {count} viral hooks for: {topic}
        Use these successful structures as inspiration: {best_hooks[:2]}
        Tone: Sovereign and Avant-garde.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        )
        
        return [h.strip() for h in response.text.split("\n") if h.strip()]
