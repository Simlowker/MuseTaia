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
    target_img = b"fake_target_image"
    ref_imgs = [b"ref_1", b"ref_2"]
    
    report = agent.verify_consistency(target_img, ref_imgs)
    
    assert report.is_consistent is False
    assert report.score == 0.6
    assert report.feedback[0].category == "lighting"
    
    # Verify the call to generate_content
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args
    # 2 refs + 1 target + 1 prompt = 4 parts
    assert len(call_args.kwargs["contents"][0].parts) == 4

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
