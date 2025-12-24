"""Tests for the StrategistAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.strategist import StrategistAgent

@pytest.fixture
def mock_genai_client():
    with patch("app.agents.strategist.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_strategist_initialization(mock_genai_client):
    strategist = StrategistAgent()
    assert strategist.model_name == "gemini-3-pro-preview"

def test_define_strategy(mock_genai_client):
    strategist = StrategistAgent()
    
    # Mock response
    mock_response = MagicMock()
    mock_response.text = '{"narrative_angle": "Cyber-Sovereignty", "estimated_credits": 200}'
    strategist.client.models.generate_content.return_value = mock_response
    
    # Mock DNA
    mock_dna = MagicMock()
    mock_dna.identity.moral_graph.autonomy = 0.8
    
    strategy = strategist.define_strategy("Sample Intent", mock_dna)
    
    assert strategy["narrative_angle"] == "Cyber-Sovereignty"
    assert strategy["estimated_credits"] == 200

def test_evaluate_production_roi():
    strategist = StrategistAgent()
    
    # ROI = VVS / Cost > 50.0
    # 100 / 1.0 = 100 (> 50)
    assert strategist.evaluate_production_roi(100.0, 1.0) is True
    
    # 40 / 1.0 = 40 (< 50)
    assert strategist.evaluate_production_roi(40.0, 1.0) is False
