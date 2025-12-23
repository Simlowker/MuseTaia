"""Tests for the TrendScanner Agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.trend_scanner import TrendScanner
from app.core.schemas.trend import TrendReport, RelevanceScore, Sentiment, IntentObject, TrendType

@pytest.fixture
def mock_genai():
    with patch("app.agents.trend_scanner.genai") as mock_gen:
        yield mock_gen

@pytest.fixture
def mock_search_service():
    with patch("app.agents.trend_scanner.SearchService") as mock_search:
        yield mock_search.return_value

def test_analyze_hot_topic(mock_genai, mock_search_service):
    """Test analysis of a relevant topic resulting in an IntentObject."""
    mock_client = mock_genai.Client.return_value
    
    # Mock Search
    mock_search_service.search.return_value = "Paris Fashion Week is showcasing digital couture."
    
    # Mock Analysis
    mock_intent = IntentObject(
        command="produce_content",
        trend_type=TrendType.FASHION,
        urgency="high",
        target_audience="luxury-segment",
        raw_intent="Create a digital fashion piece for PFW",
        parameters={"--style": "minimalist"}
    )
    
    mock_report = TrendReport(
        topic="Paris Fashion Week",
        summary="Digital couture showcase",
        sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.HIGH,
        reasoning="Fits fashion focus",
        intent=mock_intent,
        keywords=["#PFW", "#DigitalFashion"],
        source_links=[]
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_report
    mock_client.models.generate_content.return_value = mock_response
    
    scanner = TrendScanner()
    result = scanner.analyze_trend("Paris Fashion Week")
    
    assert result.relevance == RelevanceScore.HIGH
    assert result.intent.command == "produce_content"
    assert result.intent.trend_type == TrendType.FASHION
    mock_search_service.search.assert_called_once()


def test_analyze_blocked_topic(mock_genai, mock_search_service):
    """Test filtering of a blocked/controversial topic."""
    mock_client = mock_genai.Client.return_value
    
    # Mock Search
    mock_search_service.search.return_value = "A heated political debate is occurring."
    
    # Mock Analysis
    mock_report = TrendReport(
        topic="Political Debate",
        summary="Controversy",
        sentiment=Sentiment.CONTROVERSIAL,
        relevance=RelevanceScore.BLOCKED,
        reasoning="Violates political constraints",
        keywords=[],
        source_links=[]
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_report
    mock_client.models.generate_content.return_value = mock_response
    
    scanner = TrendScanner()
    result = scanner.analyze_trend("Political Debate")
    
    assert result.relevance == RelevanceScore.BLOCKED
    assert result.sentiment == Sentiment.CONTROVERSIAL