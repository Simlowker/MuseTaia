"""Tests for TrendScout VVS discovery and ROI Intelligence."""

import pytest
import time
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.trend_scout import TrendScout
from app.core.schemas.market_intelligence import TrendInsight

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
    with patch("app.agents.trend_scout.ApifyClientAsync") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        # Mock settings for token
        with patch("app.agents.trend_scout.settings") as mock_settings:
            mock_settings.APIFY_TOKEN = "fake-token"
            
            scout = TrendScout()
            scout.vvs_threshold = 100.0
            
            # Mock Actor Run
            mock_actor = mock_client.actor.return_value
            mock_actor.call = AsyncMock(return_value={"defaultDatasetId": "ds-123"})
            
            # Mock Dataset items
            mock_dataset = mock_client.dataset.return_value
            now = time.time()
            items = [
                # Should be filtered out (VVS too low)
                {"id": "low", "title": "Low Trend", "upvotes": 10, "created_utc": now - 3600, "num_comments": 1},
                # Should be included (VVS high)
                {"id": "high", "title": "High Trend", "upvotes": 1000, "created_utc": now - 3600, "num_comments": 100}
            ]
            
            async def mock_iterate():
                for item in items:
                    yield item
            
            mock_dataset.iterate_items = mock_iterate
            
            insights = await scout.scan_niche(["tech"])
            
            assert len(insights) == 1
            assert insights[0].trend_fingerprint == "high"
            assert insights[0].vvs_score > 100.0