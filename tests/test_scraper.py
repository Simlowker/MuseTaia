"""Tests for the ScraperService."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.services.scraper import ScraperService

@pytest.mark.asyncio
async def test_scraper_service_initialization():
    scraper = ScraperService()
    assert scraper is not None

@pytest.mark.asyncio
async def test_scrape_platform_reddit():
    scraper = ScraperService()
    with patch.object(scraper, 'scrape_reddit', new_callable=AsyncMock) as mock_reddit:
        mock_reddit.return_value = [{"title": "test", "platform": "reddit"}]
        results = await scraper.scrape_platform("reddit", "test")
        assert len(results) > 0
        assert results[0]["title"] == "test"

@pytest.mark.asyncio
async def test_scrape_platform_tiktok():
    scraper = ScraperService()
    with patch.object(scraper, 'scrape_tiktok', new_callable=AsyncMock) as mock_tiktok:
        mock_tiktok.return_value = [{"title": "test", "platform": "tiktok"}]
        results = await scraper.scrape_platform("tiktok", "test")
        assert len(results) > 0
        assert results[0]["title"] == "test"

@pytest.mark.asyncio
async def test_scrape_platform_unknown():
    scraper = ScraperService()
    results = await scraper.scrape_platform("unknown", "test")
    assert len(results) == 0
