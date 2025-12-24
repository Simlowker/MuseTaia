"""TrendScout Agent using real-world ScraperService and VVS algorithm."""

import math
import logging
import time
import asyncio
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.services.scraper import ScraperService
from app.core.schemas.trend import TrendReport, ViralVelocity
from app.core.vertex_init import get_genai_client
from google.genai import types

logger = logging.getLogger(__name__)

class TrendScout:
    """Agent de perception proactif utilisant des données réelles et l'algorithme VVS."""

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.client = get_genai_client()
        self.model_name = model_name
        self.scraper = ScraperService()
        self.vvs_threshold = 50.0

    def calculate_vvs(self, upvotes: int, time_delta_hours: float, comments: int) -> float:
        """Calcule le Viral Velocity Score selon le Blueprint SMOS v2."""
        velocity = upvotes / max(time_delta_hours, 0.1)
        engagement_weight = math.log10(comments + 1)
        return round(velocity * engagement_weight, 2)

    async def scout_and_filter(self, topic: str) -> TrendReport:
        """Scouts platforms and filters for niche appeal using real data."""
        # Parallel scraping
        reddit_task = self.scraper.scrape_reddit(topic)
        tiktok_task = self.scraper.scrape_tiktok(topic)
        
        raw_signals = await asyncio.gather(reddit_task, tiktok_task)
        flat_signals = [item for sublist in raw_signals for item in sublist]

        # 1. Logic for VVS calculation on real signals
        total_vvs = 0.0
        now = time.time()
        for s in flat_signals:
            if s["platform"] == "reddit":
                age = (now - s.get("created_utc", now)) / 3600
                total_vvs += self.calculate_vvs(s["upvotes"], age, s["num_comments"])
        
        avg_vvs = total_vvs / max(len(flat_signals), 1)
        vvs_metrics = ViralVelocity(
            score=min(avg_vvs / 10, 10.0),
            acceleration="Rising" if avg_vvs > 50 else "Stagnant",
            engagement_rate=avg_vvs
        )

        # 2. Strategic Filtering via LLM
        signals_context = "\n".join([f"- {s.get('title')}" for s in flat_signals[:10]])
        
        prompt = f"""
        Analyze these REAL social signals for the topic: {topic}
        SIGNALS:
        {signals_context}
        
        VVS Score calculated: {vvs_metrics.score}/10. 
        
        TASK:
        Determine if this trend fits the Muse's high-fashion/tech persona.
        Assign an estimated_roi and generate an intent if VVS > 5.
        """

        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TrendReport
            )
        )

        report = response.parsed
        report.vvs = vvs_metrics
        return report

    async def scan_niche(self, niche_keywords: List[str]) -> List[Any]:
        """Scanne les niches pour le daemon de surveillance."""
        # Simplification: we reuse scout_and_filter for each keyword
        results = []
        for kw in niche_keywords:
            report = await self.scout_and_filter(kw)
            if report.vvs.score > 5.0:
                results.append(report)
        return results