"""TrendScanner Agent for analyzing topics and filtering opportunities."""

import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.core.services.search_service import SearchService
from app.core.schemas.trend import TrendReport, RelevanceScore

class TrendScanner:
    """Agent that perceives trends and evaluates their fit for the Muse."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the TrendScanner.

        Args:
            model_name: The name of the Gemini model to use.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.search_service = SearchService(model_name=model_name)

    def analyze_trend(self, topic: str, persona_constraints: str = "Avoid political controversy. Focus on fashion, tech, and art.") -> TrendReport:
        """Analyzes a topic using real-time search data and persona constraints.

        Args:
            topic: The trend or topic to analyze.
            persona_constraints: Guidelines for what fits the Muse's identity.

        Returns:
            TrendReport: Structured analysis.
        """
        
        # 1. Gather Context via Search
        # We perform a search to get the latest info on the topic
        search_summary = self.search_service.search(f"What is the current sentiment and context for: {topic}?")
        
        # 2. Evaluate using Gemini
        prompt = f"""
        Analyze the following topic based on the provided search context and persona constraints.
        
        Topic: {topic}
        Search Context: {search_summary}
        
        Persona Constraints: {persona_constraints}
        
        Determine the relevance, sentiment, and provide a reasoning.
        If the topic violates constraints or is negative/controversial in a way that risks the brand, mark relevance as BLOCKED.
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

        report = response.parsed
        # Manually attach grounding metadata source links if available in future SDK versions
        # For now we rely on the model filling the list if it used internal knowledge, 
        # but ideally we would merge `search_service` sources here.
        
        return report
