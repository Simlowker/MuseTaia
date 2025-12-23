"""Tests for Governance Lobe (Critic & CFO)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent
from app.agents.finance_agent import CFOAgent
from app.core.schemas.qa import QAReport
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory

@pytest.fixture
def mock_genai():
    with patch("app.agents.critic_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_critic_consistency_strict_rule(mock_genai):
    critic = CriticAgent()
    mock_response = MagicMock()
    # Align with actual QAReport used in code
    mock_report = QAReport(
        is_consistent=True,
        identity_drift_score=0.99,
        clip_semantic_score=1.0,
        failures=[],
        final_decision="APPROVED"
    )
    # The actual implementation calls detect_physical_artifacts which also uses the client
    # Let's mock the responses sequentially or simplify
    critic.client.models.generate_content.return_value.parsed = [] # No artifacts
    
    # Mock face similarity (which uses VisualComparator, not GenAI directly in current code)
    with patch("app.agents.critic_agent.VisualComparator.calculate_face_similarity", return_value=0.99):
        report = critic.verify_consistency(b"target", b"ref")
    
    assert report.identity_drift_score >= 0.75 # Threshold
    assert report.is_consistent is True
    assert report.final_decision == "APPROVED"

def test_finance_settlement():
    with patch("app.agents.finance_agent.LedgerService") as mock_ls:
        mock_service = mock_ls.return_value
        expected_tx = Transaction(
            transaction_id="tx-123",
            amount=50.0,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.API_COST,
            description="Production cost settlement for task: test-task"
        )
        mock_service.record_transaction.return_value = expected_tx
        
        finance = CFOAgent()
        tx = finance.settle_production_cost(50, "test-task")
        
        assert tx.amount == 50.0
        assert tx.type == TransactionType.EXPENSE
        mock_service.record_transaction.assert_called_once()