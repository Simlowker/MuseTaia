"""Real-world Scraper service using Apify Client."""

import logging
from typing import List, Dict, Any, Optional
from apify_client import ApifyClientAsync
from app.core.config import settings

logger = logging.getLogger(__name__)

class ScraperService:
    """Service to handle real social scraping requests via Apify.
    
    This replaces the previous mock implementation with real Actor calls.
    """

    def __init__(self):
        self.client = ApifyClientAsync(token=settings.APIFY_TOKEN)

    async def scrape_reddit(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Scrapes Reddit for viral signals using a real Apify Actor."""
        if not settings.APIFY_TOKEN:
            return []

        logger.info(f"APIFY: Scraping Reddit for '{query}'...")
        try:
            # Using the popular Reddit Scraper actor
            run = await self.client.actor("trudax/reddit-scraper").call(
                run_input={
                    "search": query,
                    "type": "link",
                    "sort": "relevance",
                    "time": "day",
                    "maxItems": limit
                }
            )
            
            results = []
            async for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "upvotes": item.get("ups", 0),
                    "num_comments": item.get("num_comments", 0),
                    "created_utc": item.get("created_utc"),
                    "url": item.get("url"),
                    "platform": "reddit"
                })
            return results
        except Exception as e:
            logger.error(f"APIFY: Reddit scrape failed: {e}")
            return []

    async def scrape_tiktok(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Scrapes TikTok for trends using a real Apify Actor."""
        logger.info(f"APIFY: Scraping TikTok for '{query}'...")
        try:
            run = await self.client.actor("clockworks/tiktok-scraper").call(
                run_input={
                    "hashtags": [query.replace(" ", "")],
                    "resultsPerPage": limit,
                    "shouldDownloadVideo": False
                }
            )
            
            results = []
            async for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append({
                    "id": item.get("id"),
                    "title": item.get("desc"),
                    "views": item.get("stats", {}).get("playCount", 0),
                    "likes": item.get("stats", {}).get("diggCount", 0),
                    "platform": "tiktok"
                })
            return results
        except Exception as e:
            logger.error(f"APIFY: TikTok scrape failed: {e}")
            return []