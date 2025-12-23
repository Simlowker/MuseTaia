"""Tests for the CriticAgent and Visual QA logic (Governance v3)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent
from app.core.schemas.qa import QAReport

@pytest.fixture
def mock_genai():
    with patch("google.genai.Client") as mock_gen:
        yield mock_gen

def test_critic_2_percent_rule_approval(mock_genai):
    """Tests that a high similarity score results in APPROVAL."""
    critic = CriticAgent()
    # Mock high similarity (0.99 > 0.75)
    with patch.object(critic.comparator, "calculate_face_similarity", return_value=0.99):
        report = critic.verify_consistency(b"target", b"ref")
        assert report.final_decision == "APPROVED"
        assert report.is_consistent is True

def test_critic_identity_drift_repair(mock_genai):
    """Tests that a moderate drift triggers REPAIR_REQUIRED."""
    critic = CriticAgent()
    # Mock moderate similarity (0.65 < 0.75)
    with patch.object(critic.comparator, "calculate_face_similarity", return_value=0.65):
        report = critic.verify_consistency(b"target", b"ref")
        assert report.final_decision == "REPAIR_REQUIRED"
        assert len(report.failures) > 0
        assert report.failures[0].action_type == "inpaint"

def test_critic_mask_detection(mock_genai):
    """Tests that Critic correctly requests mask detection for repairs."""
    critic = CriticAgent()
    mock_response = MagicMock()
    mock_response.parsed.box_2d = [100, 100, 200, 200]
    critic.client.models.generate_content.return_value = mock_response
    
    bbox = critic.detect_mask_area(b"image", "face")
    assert bbox == [100, 100, 200, 200]
