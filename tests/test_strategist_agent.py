"""Tests for the StrategistAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.strategist import StrategistAgent

@pytest.fixture
def mock_genai_client():
    with patch("google.genai.Client") as mock_client:
        yield mock_client

def test_strategist_initialization(mock_genai_client):
    strategist = StrategistAgent()
    assert strategist.model_name == "gemini-3.0-flash-preview"

def test_define_strategy(mock_genai_client):
    strategist = StrategistAgent()
    
    # Mock response
    mock_response = MagicMock()
    mock_response.text = '{"narrative_angle": "Cyber-Sovereignty", "estimated_credits": 200}'
    strategist.client.models.generate_content.return_value = mock_response
    
    strategy = strategist.define_strategy("Sample Intent")
    
    assert strategy["narrative_angle"] == "Cyber-Sovereignty"
    assert strategy["estimated_credits"] == 200

def test_evaluate_production_roi():
    strategist = StrategistAgent()
    
    # Trend score 9, cost 80 -> Approved (90 >= 80)
    assert strategist.evaluate_production_roi(9.0, 80) is True
    
    # Trend score 5, cost 200 -> Rejected (50 < 200)
    assert strategist.evaluate_production_roi(5.0, 200) is False
