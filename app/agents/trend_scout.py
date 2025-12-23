"""TrendScout Agent using Apify and the Viral Velocity Score (VVS) algorithm."""

import math
import logging
import time
from typing import List, Optional, Dict, Any
from apify_client import ApifyClientAsync
from app.core.config import settings
from app.core.schemas.market_intelligence import TrendInsight

logger = logging.getLogger(__name__)

class TrendScout:
    """Agent de perception proactif utilisant Apify et l'algorithme VVS.
    
    This agent represents the 'Scout Lobe' (v2).
    It filters social signals based on mathematical velocity to maximize ROI.
    """

    def __init__(self):
        self.client = ApifyClientAsync(token=settings.APIFY_TOKEN)
        self.vvs_threshold = 50.0 # Seuil de déclenchement proactif

    def calculate_vvs(self, upvotes: int, time_delta_hours: float, comments: int) -> float:
        """Calcule le Viral Velocity Score selon le Blueprint SMOS v2.
        
        Formula: VVS = (Delta Upvotes / Delta Time) * log10(CommentVolume + 1)
        """
        velocity = upvotes / max(time_delta_hours, 0.1)
        engagement_weight = math.log10(comments + 1)
        return round(velocity * engagement_weight, 2)

    async def scan_niche(self, niche_keywords: List[str]) -> List[TrendInsight]:
        """Scanne Reddit pour identifier des signaux faibles à forte vélocité."""
        insights = []
        
        if not settings.APIFY_TOKEN:
            logger.warning("APIFY_TOKEN not set. Returning empty insights.")
            return []

        try:
            # 1. Lancement de l'Actor Reddit (Scraping réactif)
            # Utilise l'actor standard ou spécifié dans le blueprint
            actor_run = await self.client.actor("agentx/reddit-viral-scraper").call(
                run_input={
                    "searchKeywords": " ".join(niche_keywords),
                    "sort": "relevance",
                    "time": "day",
                    "limit": 50
                }
            )

            # 2. Post-traitement et filtrage Signal-to-Noise
            dataset_id = actor_run.get("defaultDatasetId")
            async for item in self.client.dataset(dataset_id).iterate_items():
                upvotes = item.get("upvotes", 0)
                created_at = item.get("created_utc", 0)
                comments = item.get("num_comments", 0)
                
                # Calcul de l'âge du post en heures
                age_hours = (time.time() - created_at) / 3600

                vvs = self.calculate_vvs(upvotes, age_hours, comments)

                # 3. Filtrage par seuil de vélocité (VVS)
                if vvs > self.vvs_threshold:
                    insights.append(TrendInsight(
                        trend_fingerprint=str(item.get("id")),
                        topic=item.get("title", "Unknown"),
                        vvs_score=vvs,
                        platform="reddit",
                        sentiment_index=0.5, # Placeholder pour enrichissement futur
                        visual_context_urls=[item.get("url")] if item.get("url") else [],
                        suggested_intent=f"produce --trend '{item.get('title')}' --vvs {vvs}"
                    ))
        except Exception as e:
            logger.error(f"TrendScout: Failed to scan niche: {e}")

        return sorted(insights, key=lambda x: x.vvs_score, reverse=True)
