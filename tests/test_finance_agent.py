"""Tests for the FinanceAgent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.finance_agent import FinanceAgent, FinancialSummary
from app.state.models import Wallet
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory

@pytest.fixture
def mock_genai():
    with patch("app.agents.finance_agent.genai") as mock_gen:
        yield mock_gen

def test_summarize_health(mock_genai):
    """Test that the finance agent generates a summary correctly."""
    mock_client = mock_genai.Client.return_value
    
    # Mock Response
    mock_summary = FinancialSummary(
        balance_usd=100.0,
        recent_expenses=5.0,
        burn_rate_estimate="Low",
        advice="Keep producing high quality content.",
        status="healthy"
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_summary
    mock_client.models.generate_content.return_value = mock_response
    
    agent = FinanceAgent()
    wallet = Wallet(address="gen", balance=1.0, internal_usd_balance=100.0)
    history = [
        Transaction(transaction_id="1", type=TransactionType.EXPENSE, category=TransactionCategory.API_COST, amount=0.5, description="test")
    ]
    
    summary = agent.summarize_health(wallet, history)
    
    assert summary.status == "healthy"
    assert "Keep producing" in summary.advice
    mock_client.models.generate_content.assert_called_once()
