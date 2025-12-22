"""Tests for the CriticAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent, ConsistencyReport

@pytest.fixture
def mock_genai():
    with patch("app.agents.critic_agent.genai") as mock_gen:
        yield mock_gen

def test_critic_agent_verify_consistency(mock_genai):
    """Tests that The Critic correctly processes and parses image comparison results."""
    mock_client = mock_genai.Client.return_value
    
    # Mock the parsed response
    mock_report = ConsistencyReport(
        is_consistent=True,
        score=0.95,
        issues=[],
        recommendations="Everything looks perfect."
    )
    
    mock_response = MagicMock()
    mock_response.parsed = mock_report
    mock_client.models.generate_content.return_value = mock_response
    
    agent = CriticAgent()
    
    # Dummy image bytes
    img1 = b"fake_reference_image"
    img2 = b"fake_target_image"
    
    report = agent.verify_consistency(img1, img2)
    
    assert report.is_consistent is True
    assert report.score == 0.95
    assert len(report.issues) == 0
    
    # Verify the call to generate_content
    mock_client.models.generate_content.assert_called_once()
    call_args = mock_client.models.generate_content.call_args
    assert call_args.kwargs["model"] == "gemini-2.0-flash"
    assert len(call_args.kwargs["contents"][0].parts) == 3
