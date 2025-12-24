"""Tests for TrendScout VVS discovery and ROI Intelligence."""

import pytest
import time
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.trend_scout import TrendScout

def test_vvs_formula():
    """Tests the mathematical correctness of the VVS formula."""
    scout = TrendScout()
    
    # post: 100 upvotes, 2 hours old, 9 comments
    # velocity = 100 / 2 = 50
    # weight = log10(9 + 1) = 1.0
    # VVS = 50 * 1 = 50.0
    vvs = scout.calculate_vvs(100, 2.0, 9)
    assert vvs == 50.0

    # high engagement: 1000 upvotes, 1 hour old, 99 comments
    # velocity = 1000
    # weight = log10(100) = 2.0
    # VVS = 2000.0
    vvs_high = scout.calculate_vvs(1000, 1.0, 99)
    assert vvs_high == 2000.0

@pytest.mark.asyncio
async def test_scan_niche_filtering():
    """Tests that scan_niche correctly filters and sorts insights."""
    with patch("app.core.services.scraper.ApifyClientAsync") as mock_client_cls, \
         patch("app.agents.trend_scout.get_genai_client") as mock_genai_get:
        
        mock_client = mock_client_cls.return_value
        mock_genai = MagicMock()
        mock_genai_get.return_value = mock_genai
        
        # Mock settings for token
        with patch("app.agents.trend_scout.settings") as mock_settings:
            mock_settings.APIFY_TOKEN = "fake-token"
            
            scout = TrendScout()
            scout.vvs_threshold = 5.0 # Threshold in scout_and_filter logic
            
            # Mock Scraper results
            now = time.time()
            items = [
                {"id": "low", "title": "Low", "upvotes": 1, "created_utc": now, "num_comments": 0, "platform": "reddit"},
                {"id": "high", "title": "High", "upvotes": 1000, "created_utc": now - 3600, "num_comments": 100, "platform": "reddit"}
            ]
            
            async def mock_reddit(topic, limit=10): return items
            async def mock_tiktok(topic, limit=5): return []
            
            with patch.object(scout.scraper, 'scrape_reddit', side_effect=mock_reddit), \
                 patch.object(scout.scraper, 'scrape_tiktok', side_effect=mock_tiktok):
                
                # Mock LLM response
                from app.core.schemas.trend import TrendReport, RelevanceScore, Sentiment
                mock_report = TrendReport(
                    topic="High", summary="S", sentiment=Sentiment.POSITIVE, 
                    relevance=RelevanceScore.HIGH, reasoning="R"
                )
                mock_genai.models.generate_content.return_value.parsed = mock_report
                
                insights = await scout.scan_niche(["tech"])
                
                assert len(insights) == 1
                assert insights[0].topic == "High"