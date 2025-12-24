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
    
    # Mock Redis pipeline for WATCH/MULTI
    mock_pipeline = MagicMock()
    mock_deps["redis"].pipeline.return_value.__enter__.return_value = mock_pipeline
    mock_pipeline.get.return_value = initial_wallet.model_dump_json().encode('utf-8')
    
    # Record expense
    service.record_transaction(
        wallet_address=addr,
        tx_type=TransactionType.EXPENSE,
        category=TransactionCategory.API_COST,
        amount=0.50,
        description="Test cost"
    )
    
    # Verify pipeline execution
    mock_pipeline.multi.assert_called_once()
    mock_pipeline.execute.assert_called_once()
    
    # Verify balance update
    set_args = mock_pipeline.set.call_args.args
    assert addr in set_args[0]
    updated_wallet = Wallet.model_validate_json(set_args[1])
    assert updated_wallet.internal_usd_balance == 9.50

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
