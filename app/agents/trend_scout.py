"""TrendScout Agent for social scraping and niche filtering with VVS."""

import google.genai as genai
from google.genai import types
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.services.scraper import ScraperService
from app.core.schemas.trend import TrendReport, ViralVelocity

class TrendScout:
    """Agent that scouts social platforms and filters niche trends.
    
    This agent represents the 'Scout Lobe'.
    v2: Includes the Viral Velocity Score (VVS) algorithm.
    """

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the TrendScout."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name
        self.scraper = ScraperService()

    def _calculate_vvs(self, signals: List[Dict[str, Any]]) -> ViralVelocity:
        """Calculates the Viral Velocity Score from raw signals.
        
        Algorithm: VVS = (Average Engagement) * (Acceleration Factor)
        """
        if not signals:
            return ViralVelocity(score=0.0, acceleration="Stagnant", engagement_rate=0.0)
            
        total_engagement = 0
        for s in signals:
            # Normalize different metrics (likes, views, etc.)
            total_engagement += s.get("engagement", 0)
            total_engagement += s.get("likes", 0) / 10 # Normalize likes to engagement weight
            total_engagement += s.get("views", 0) / 1000 # Normalize views
            
        avg_engagement = total_engagement / len(signals)
        
        # Heuristic for acceleration based on engagement levels
        # In a real system, we'd compare against historical snapshots.
        acceleration = "Stagnant"
        score = min(avg_engagement / 100, 10.0) # Map to 0-10 scale
        
        if score > 7.0:
            acceleration = "Peaking"
        elif score > 3.0:
            acceleration = "Rising"
            
        return ViralVelocity(
            score=round(score, 2),
            acceleration=acceleration,
            engagement_rate=round(avg_engagement, 2)
        )

    def scout_and_filter(self, topic: str, platforms: Optional[List[str]] = None) -> TrendReport:
        """Scouts multiple platforms and filters the results for niche appeal with VVS."""
        if platforms is None:
            platforms = ["twitter", "instagram", "tiktok"]

        raw_signals = []
        for platform in platforms:
            signals = self.scraper.scrape_platform(platform, topic)
            raw_signals.extend(signals)

        # 1. Calculate VVS (Imperative Logic)
        vvs_metrics = self._calculate_vvs(raw_signals)

        # 2. Format signals for the model
        signals_context = ""
        for i, signal in enumerate(raw_signals):
            signals_context += f"Signal {i+1}: {signal}\n"
        
        prompt = f"""
        You are the 'TrendScout' for the Muse.
        Your role is to perform 'Niche Filtering' using the Viral Velocity Score.
        
        VIRAL VELOCITY METRICS:
        - Score: {vvs_metrics.score}/10
        - Acceleration: {vvs_metrics.acceleration}
        - Engagement Rate: {vvs_metrics.engagement_rate}
        
        We are looking for emerging, sophisticated trends that align with 
        a high-fashion, autonomous, and tech-pioneering persona.
        
        Interest Area: {topic}
        Raw Social Signals:
        {signals_context}
        
        TASK:
        1. Analyze the signals for a specific niche trend.
        2. Assign an 'estimated_roi' (Engagement Score / Production Cost). 
           - High velocity + Niche appeal = High ROI.
        3. If a high-value opportunity is found, generate an intent.
        
        Return the result as a TrendReport including the VVS metrics provided.
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
        report.vvs = vvs_metrics # Ensure exact metrics are preserved
        return report