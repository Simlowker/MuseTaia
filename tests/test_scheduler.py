"""Tests for the ProactiveScheduler."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.scheduler import ProactiveScheduler
from app.core.schemas.trend import TrendReport, RelevanceScore, Sentiment
from app.state.models import Mood

@pytest.fixture
def mock_components():
    with patch("app.core.scheduler.TrendScanner") as m_scanner, \
         patch("app.core.scheduler.WorkflowEngine") as m_engine:
        yield {
            "scanner": m_scanner.return_value,
            "engine": m_engine.return_value
        }

def test_scan_triggers_production(mock_components):
    """Test that a HIGH relevance trend triggers the workflow engine."""
    scheduler = ProactiveScheduler()
    
    # Mock Analysis: 1 High, 1 Low
    high_report = TrendReport(
        topic="Digital Fashion",
        summary="NFTs are hot",
        sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.HIGH,
        reasoning="Good fit"
    )
    low_report = TrendReport(
        topic="Boring Stuff",
        summary="Yawn",
        sentiment=Sentiment.NEUTRAL,
        relevance=RelevanceScore.LOW,
        reasoning="Boring"
    )
    
    mock_components["scanner"].analyze_trend.side_effect = [high_report, low_report]
    
    # Mock Workflow
    mock_components["engine"].produce_video_content.return_value = {"status": "success"}
    
    # Only test with 2 topics to match our side_effect
    scheduler.interest_topics = ["Digital Fashion", "Boring Stuff"]
    
    mood = Mood(valence=0.8)
    results = scheduler.scan_and_activate(subject_id="genesis", current_mood=mood)
    
    assert len(results) == 1
    assert results[0]["topic"] == "Digital Fashion"
    assert results[0]["status"] == "produced"
    
    # Verify calls
    assert mock_components["scanner"].analyze_trend.call_count == 2
    mock_components["engine"].produce_video_content.assert_called_once()
    
    # Check intent construction
    call_args = mock_components["engine"].produce_video_content.call_args
    assert "NFTs are hot" in call_args.kwargs["intent"]

def test_scan_skips_low_relevance(mock_components):
    """Test that LOW relevance trends are ignored."""
    scheduler = ProactiveScheduler()
    
    low_report = TrendReport(
        topic="Boring",
        summary="...",
        sentiment=Sentiment.NEUTRAL,
        relevance=RelevanceScore.LOW,
        reasoning="..."
    )
    mock_components["scanner"].analyze_trend.return_value = low_report
    
    scheduler.interest_topics = ["Boring"]
    mood = Mood(valence=0.5)
    results = scheduler.scan_and_activate("genesis", mood)
    
    assert len(results) == 0
    mock_components["engine"].produce_video_content.assert_not_called()
