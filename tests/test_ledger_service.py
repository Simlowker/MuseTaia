"""Tests for the LedgerService."""

import pytest
import json
from unittest.mock import MagicMock, patch
from app.core.services.ledger_service import LedgerService
from app.core.schemas.finance import TransactionType, TransactionCategory
from app.state.models import Wallet

@pytest.fixture
def mock_deps():
    with patch("app.core.services.ledger_service.get_redis_client") as m_redis, \
         patch("app.core.services.ledger_service.StateManager") as m_state:
        yield {
            "redis": m_redis.return_value,
            "state": m_state.return_value
        }

def test_record_expense(mock_deps):
    service = LedgerService()
    addr = "test_wallet"
    
    # Setup mock wallet
    initial_wallet = Wallet(address=addr, balance=1.0, internal_usd_balance=10.0)
    mock_deps["state"].get_wallet.return_value = initial_wallet
    
    # Record expense
    service.record_transaction(
        wallet_address=addr,
        tx_type=TransactionType.EXPENSE,
        category=TransactionCategory.API_COST,
        amount=0.50,
        description="Test cost"
    )
    
    # Verify balance update
    mock_deps["state"].update_wallet.assert_called_once()
    updated_wallet = mock_deps["state"].update_wallet.call_args.args[0]
    assert updated_wallet.internal_usd_balance == 9.50
    
    # Verify history push
    mock_deps["redis"].rpush.assert_called_once()
    history_args = mock_deps["redis"].rpush.call_args
    assert addr in history_args.args[0]
    assert "0.5" in history_args.args[1]

def test_get_history(mock_deps):
    service = LedgerService()
    addr = "test_wallet"
    
    # Mock some history records
    record = {
        "transaction_id": "tx1",
        "type": "income",
        "category": "sponsorship",
        "amount": 5.0,
        "description": "Gift",
        "timestamp": "2025-12-22T12:00:00Z"
    }
    mock_deps["redis"].lrange.return_value = [json.dumps(record).encode('utf-8')]
    
    history = service.get_transaction_history(addr)
    assert len(history) == 1
    assert history[0].transaction_id == "tx1"
    assert history[0].amount == 5.0
