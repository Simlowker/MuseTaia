"""Tests for the TrendScout agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.trend_scout import TrendScout
from app.core.schemas.trend import TrendReport, RelevanceScore, Sentiment

@pytest.fixture
def mock_genai_client():
    with patch("google.genai.Client") as mock_client:
        yield mock_client

def test_trend_scout_initialization(mock_genai_client):
    scout = TrendScout()
    assert scout.model_name == "gemini-3.0-flash-preview"
    assert scout.scraper is not None

def test_scout_and_filter(mock_genai_client):
    scout = TrendScout()
    
    # Mock the response from Gemini
    mock_response = MagicMock()
    mock_report = TrendReport(
        topic="Cyber-Baroque Fashion",
        summary="An emerging niche blending 17th-century aesthetics with futuristic tech materials.",
        sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.HIGH,
        reasoning="High alignment with Muse's avant-garde and tech-forward persona.",
        source_links=["https://twitter.com/niche_trend"]
    )
    mock_response.parsed = mock_report
    scout.client.models.generate_content.return_value = mock_response
    
    report = scout.scout_and_filter("fashion")
    
    assert report.topic == "Cyber-Baroque Fashion"
    assert report.relevance == RelevanceScore.HIGH
    assert scout.client.models.generate_content.called
