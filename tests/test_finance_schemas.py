"""Tests for the financial schemas."""

import pytest
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory
from app.state.models import Wallet

def test_transaction_validation():
    """Test creating a valid transaction."""
    tx = Transaction(
        transaction_id="tx_123",
        type=TransactionType.EXPENSE,
        category=TransactionCategory.API_COST,
        amount=0.05,
        description="Gemini 3 Pro call"
    )
    assert tx.amount == 0.05
    assert tx.type == "expense"

def test_wallet_update():
    """Test updating the wallet model."""
    wallet = Wallet(
        address="muse_wallet_addr",
        balance=10.0,
        internal_usd_balance=100.0
    )
    assert wallet.internal_usd_balance == 100.0
    wallet.internal_usd_balance -= 0.50
    assert wallet.internal_usd_balance == 99.50
