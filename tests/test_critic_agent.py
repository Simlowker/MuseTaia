"""Tests for the CriticAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent
from app.core.schemas.qa import QAReport, QAFailure

@pytest.fixture
def mock_genai():
    with patch("app.agents.critic_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_critic_agent_verify_consistency(mock_genai):
    """Tests that The Critic correctly processes and parses image comparison results."""
    mock_client = mock_genai
    
    # Mock face similarity
    with patch("app.agents.critic_agent.VisualComparator.calculate_face_similarity", return_value=0.9):
        # Mock artifact detection response
        mock_response = MagicMock()
        mock_response.parsed = [] # No artifacts
        mock_client.models.generate_content.return_value = mock_response
        
        agent = CriticAgent()
        
        # Dummy image bytes
        target_img = b"fake_target_image"
        ref_img = b"ref_face"
        
        report = agent.verify_consistency(target_img, ref_img)
        
        assert report.is_consistent is True
        assert report.identity_drift_score == 0.9
        assert report.final_decision == "APPROVED"

def test_detect_mask_area(mock_genai):
    """Test bounding box detection."""
    mock_client = mock_genai
    
    # Mock detection response
    mock_response = MagicMock()
    mock_result = MagicMock()
    mock_result.box_2d = [100, 200, 300, 400]
    mock_response.parsed = mock_result
    mock_client.models.generate_content.return_value = mock_response
    
    agent = CriticAgent()
    box = agent.detect_mask_area(b"img", "face")
    
    assert box == [100, 200, 300, 400]
    call_args = mock_client.models.generate_content.call_args
    assert "Detect the bounding box" in call_args.kwargs["contents"][0].parts[1].text
