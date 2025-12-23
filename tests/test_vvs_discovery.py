"""Tests for TrendScout VVS discovery and Strategist ROI evaluation."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.trend_scout import TrendScout
from app.agents.strategist import StrategistAgent
from app.core.schemas.trend import TrendReport, ViralVelocity, Sentiment, RelevanceScore

def test_vvs_calculation():
    """Tests the mathematical correctness of the VVS algorithm."""
    scout = TrendScout()
    
    # 1. Rising Trend
    signals_rising = [
        {"engagement": 500},
        {"likes": 2000}, # /10 = 200
        {"views": 300000} # /1000 = 300
    ]
    # Avg = (500 + 200 + 300) / 3 = 333.33
    # Score = 333 / 100 = 3.33
    vvs_rising = scout._calculate_vvs(signals_rising)
    assert vvs_rising.score == 3.33
    assert vvs_rising.acceleration == "Rising"

    # 2. Peaking Trend
    signals_peak = [{"engagement": 1000}] # Score = 10.0
    vvs_peak = scout._calculate_vvs(signals_peak)
    assert vvs_peak.score == 10.0
    assert vvs_peak.acceleration == "Peaking"

def test_strategist_vvs_roi():
    """Tests that Strategist approves based on VVS peaks and ROI."""
    strategist = StrategistAgent()
    
    # Peak trend should be approved even if ROI is low
    peak_report = TrendReport(
        topic="Peak", summary="X", sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.HIGH, reasoning="X", estimated_roi=0.5,
        vvs=ViralVelocity(score=10.0, acceleration="Peaking", engagement_rate=1000)
    )
    assert strategist.evaluate_production_roi(peak_report, 1.0) is True

    # High ROI trend should be approved
    high_roi_report = TrendReport(
        topic="Value", summary="X", sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.HIGH, reasoning="X", estimated_roi=1.5,
        vvs=ViralVelocity(score=2.0, acceleration="Rising", engagement_rate=200)
    )
    assert strategist.evaluate_production_roi(high_roi_report, 1.0) is True

    # Low everything should be rejected
    bad_report = TrendReport(
        topic="Bad", summary="X", sentiment=Sentiment.POSITIVE,
        relevance=RelevanceScore.LOW, reasoning="X", estimated_roi=0.1,
        vvs=ViralVelocity(score=0.1, acceleration="Stagnant", engagement_rate=10)
    )
    assert strategist.evaluate_production_roi(bad_report, 1.0) is False
