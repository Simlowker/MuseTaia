"""Tests for Governance Lobe (Critic & Finance)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.critic_agent import CriticAgent
from app.agents.finance_agent import FinanceAgent
from app.core.schemas.qa import ConsistencyReport
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory

@pytest.fixture
def mock_genai():
    with patch("google.genai.Client") as mock_gen:
        yield mock_gen

def test_critic_consistency_strict_rule(mock_genai):
    critic = CriticAgent()
    mock_response = MagicMock()
    mock_report = ConsistencyReport(
        is_consistent=True,
        score=0.99,
        issues=[],
        feedback=[],
        recommendations="Identity perfectly maintained."
    )
    mock_response.parsed = mock_report
    critic.client.models.generate_content.return_value = mock_response
    
    report = critic.verify_consistency(b"target", [b"ref"])
    
    assert report.score >= 0.98
    assert report.is_consistent is True

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
        
        finance = FinanceAgent()
        tx = finance.settle_production_cost(50, "test-task")
        
        assert tx.amount == 50.0
        assert tx.type == TransactionType.EXPENSE
        mock_service.record_transaction.assert_called_once()