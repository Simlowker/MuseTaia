"""TrendScout Agent for social scraping and niche filtering."""

import google.genai as genai
from google.genai import types
from typing import List, Optional
from app.core.config import settings
from app.core.services.scraper import ScraperService
from app.core.schemas.trend import TrendReport

class TrendScout:
    """Agent that scouts social platforms and filters niche trends.    
    This agent represents the 'Scout Lobe' in the Functional Lobe Architecture.
    It specializes in high-volume social signal gathering and specialized 
    niche filtering to find opportunities before they hit the mainstream.
    """

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the TrendScout.
        
        Args:
            model_name: The name of the model to use for filtering.
                        In production, Gemma 2 27B is used for cost-effective 
                        high-volume filtering.
        """
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.scraper = ScraperService()

    def scout_and_filter(self, topic: str, platforms: Optional[List[str]] = None) -> TrendReport:
        """Scouts multiple platforms and filters the results for niche appeal.        
        Args:
            topic: The high-level topic or interest area to scout.
            platforms: List of platforms to scrape. Defaults to twitter, instagram, tiktok.
            
        Returns:
            TrendReport: Structured analysis of the filtered niche trend.
        """
        if platforms is None:
            platforms = ["twitter", "instagram", "tiktok"]

        raw_signals = []
        for platform in platforms:
            signals = self.scraper.scrape_platform(platform, topic)
            raw_signals.extend(signals)

        # Format signals for the model
        signals_context = ""
        for i, signal in enumerate(raw_signals):
            signals_context += f"Signal {i+1}: {signal}\n"
        
        prompt = f"""
        You are the 'TrendScout' for the Muse.
        Your role is to perform 'Niche Filtering' on raw social media signals.
        
        We are NOT looking for mainstream viral content. 
        We are looking for emerging, sophisticated, or 'coded' trends that align with 
        a persona that is:
        - High-fashion and Avant-garde
        - Sovereign and Autonomous
        - Tech-pioneering
        - Digitally Native
        
        Interest Area: {topic}
        
        Raw Social Signals:
        {signals_context}
        
        TASK:
        1. Analyze the signals for a specific niche trend or micro-aesthetic.
        2. Evaluate its fit for the Muse's persona.
        3. If a high-value opportunity is found, generate an intent for content production.
        4. If the signals are too noisy or mainstream, set relevance to LOW or MEDIUM.
        
        Return the result as a TrendReport.
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
