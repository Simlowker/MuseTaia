"""Tests for the ScraperService."""

import pytest
from app.core.services.scraper import ScraperService

def test_scraper_service_initialization():
    scraper = ScraperService()
    assert scraper is not None

def test_scrape_platform_twitter():
    scraper = ScraperService()
    results = scraper.scrape_platform("twitter", "test")
    assert len(results) > 0
    assert "text" in results[0]
    assert "author" in results[0]

def test_scrape_platform_instagram():
    scraper = ScraperService()
    results = scraper.scrape_platform("instagram", "test")
    assert len(results) > 0
    assert "caption" in results[0]

def test_scrape_platform_tiktok():
    scraper = ScraperService()
    results = scraper.scrape_platform("tiktok", "test")
    assert len(results) > 0
    assert "description" in results[0]

def test_scrape_platform_unknown():
    scraper = ScraperService()
    results = scraper.scrape_platform("unknown", "test")
    assert len(results) == 1
    assert "text" in results[0]
