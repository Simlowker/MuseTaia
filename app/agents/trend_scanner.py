"""TrendScanner Agent for analyzing topics and filtering opportunities."""

import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.services.search_service import SearchService
from app.core.schemas.trend import TrendReport, RelevanceScore
from app.core.vertex_init import get_genai_client

class TrendScanner:
    """Agent that perceives trends and evaluates their fit for the Muse."""

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        """Initializes the TrendScanner.

        Args:
            model_name: The name of the Gemini model to use.
        """
        self.client = get_genai_client()
        self.model_name = model_name
        self.search_service = SearchService(model_name=model_name)

    def analyze_trend(self, topic: str, persona_constraints: str = "Avoid political controversy. Focus on fashion, tech, and art.") -> TrendReport:
        """Analyzes a topic using real-time search data and persona constraints.

        Args:
            topic: The trend or topic to analyze.
            persona_constraints: Guidelines for what fits the Muse's identity.

        Returns:
            TrendReport: Structured analysis including a proactive IntentObject.
        """
        
        # 1. Gather Context via Search
        search_summary = self.search_service.search(f"What is the current sentiment and context for: {topic}?")
        
        # 2. Evaluate using Gemini
        prompt = f"""
        Analyze the following topic based on the provided search context and persona constraints.
        
        Topic: {topic}
        Search Context: {search_summary}
        
        Persona Constraints: {persona_constraints}
        
        Your goal is to transform this external signal into a proactive system INTENT.
        
        Determine:
        1. Relevance and Sentiment.
        2. If relevance is HIGH, generate an 'intent' object that acts as a CLI command.
        
        The intent MUST include:
        - command: 'produce_content'
        - trend_type: 'fashion', 'tech', 'art', 'culture', or 'lifestyle'
        - urgency: 'low', 'medium', or 'high'
        - target_audience: 'gen-z', 'luxury-segment', 'creatives', etc.
        - parameters: Any additional flags (e.g. '--style', '--mood_modifier').
        
        If the topic violates constraints or is negative/controversial, mark relevance as BLOCKED and do not generate an intent.
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
                response_mime_type="application/json",
                response_schema=TrendReport
            )
        )

        return response.parsed
