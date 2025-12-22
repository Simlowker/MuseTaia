"""Tests for the CriticAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent
from app.core.schemas.qa import ConsistencyReport, FeedbackItem

@pytest.fixture
def mock_genai():
    with patch("app.agents.critic_agent.genai") as mock_gen:
        yield mock_gen

def test_critic_agent_verify_consistency(mock_genai):
    """Tests that The Critic correctly processes and parses image comparison results."""
    mock_client = mock_genai.Client.return_value
    
    # Mock the parsed response
    mock_report = ConsistencyReport(
        is_consistent=False,
        score=0.6,
        issues=["Lighting mismatch"],
        feedback=[
            FeedbackItem(
                category="lighting", 
                description="Too dark", 
                severity=0.8,
                action_type="inpaint",
                target_area="face"
            )
        ],
        recommendations="Brighten the face."
    )
    
    mock_response = MagicMock()
    mock_response.parsed = mock_report
    mock_client.models.generate_content.return_value = mock_response
    
    agent = CriticAgent()
    
    # Dummy image bytes
    img1 = b"fake_reference_image"
    img2 = b"fake_target_image"
    
    report = agent.verify_consistency(img1, img2)
    
    assert report.is_consistent is False
    assert report.score == 0.6
    assert report.feedback[0].category == "lighting"
    assert report.feedback[0].action_type == "inpaint"
    
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args
    assert "feedback" in call_args.kwargs["contents"][0].parts[2].text.lower()

def test_detect_mask_area(mock_genai):
    """Test bounding box detection."""
    mock_client = mock_genai.Client.return_value
    
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
    assert "bounding box" in call_args.kwargs["contents"][0].parts[1].text
