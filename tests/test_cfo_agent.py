"""Tests for the CFOAgent (Governance v2)."""

import pytest
import datetime
from unittest.mock import MagicMock, patch
from app.agents.finance_agent import CFOAgent
from app.state.models import Wallet
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory

@pytest.fixture
def mock_genai():
    with patch("app.agents.finance_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_cfo_circuit_breaker(mock_genai):
    """Tests that the circuit breaker triggers when hourly limit is exceeded."""
    agent = CFOAgent()
    wallet = Wallet(address="muse-01", balance=1000.0, internal_usd_balance=10.0)
    
    # Simulate high spend in the last hour
    now = datetime.datetime.now(datetime.timezone.utc)
    history = [
        Transaction(
            transaction_id="tx-1",
            amount=4.5,
            type=TransactionType.EXPENSE,
            category=TransactionCategory.API_COST,
            description="Prior spend",
            timestamp=now - datetime.timedelta(minutes=10)
        )
    ]
    
    # Try to spend more (Limit is 5.0)
    # 4.5 + 1.0 = 5.5 (> 5.0)
    report = agent.verify_solvency(wallet, history, 1.0)
    
    assert report.is_authorized is False
    assert report.circuit_breaker_active is True
    assert "CIRCUIT BREAKER" in report.reasoning

def test_cfo_negative_balance_prohibition(mock_genai):
    """Tests that action is forbidden if projected balance < 0."""
    agent = CFOAgent()
    wallet = Wallet(address="muse-01", balance=1000.0, internal_usd_balance=0.5) # Only 0.5 USD
    
    # Mock LLM to say 'yes' (it shouldn't matter due to hard constraint)
    mock_response = MagicMock()
    mock_response.parsed.is_authorized = True
    mock_response.parsed.reasoning = "LLM says yes"
    mock_response.parsed.projected_balance = -0.5
    agent.client.models.generate_content.return_value = mock_response
    
    report = agent.verify_solvency(wallet, [], 1.0) # 0.5 - 1.0 = -0.5
    
    assert report.is_authorized is False
    assert "PROHIBITION" in report.reasoning
    assert "Insufficient projected balance" in report.reasoning

def test_cfo_authorized_production(mock_genai):
    """Tests that CFO authorizes production when healthy."""
    agent = CFOAgent()
    wallet = Wallet(address="muse-01", balance=1000.0, internal_usd_balance=10.0)
    
    mock_response = MagicMock()
    mock_response.parsed.is_authorized = True
    mock_response.parsed.reasoning = "Strategic alignment"
    mock_response.parsed.projected_balance = 9.5
    agent.client.models.generate_content.return_value = mock_response
    
    report = agent.verify_solvency(wallet, [], 0.5)
    
    assert report.is_authorized is True
    assert report.projected_balance == 9.5