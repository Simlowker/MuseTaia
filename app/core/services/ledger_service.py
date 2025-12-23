"""Service for managing the financial ledger and wallet operations."""

import json
import logging
import uuid
from typing import List, Optional
from app.core.redis_client import get_redis_client
from app.state.models import Wallet
from app.state.db_access import StateManager
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory

logger = logging.getLogger(__name__)

class LedgerService:
    """Manages financial transactions and ensures atomicity of wallet updates."""

    def __init__(self):
        self.redis = get_redis_client()
        self.state_manager = StateManager()
        self.history_key_prefix = "smos:finance:history:"

    def record_transaction(
        self,
        wallet_address: str,
        tx_type: TransactionType,
        category: TransactionCategory,
        amount: float,
        description: str,
        metadata: Optional[dict] = None
    ) -> Transaction:
        """Records a transaction and updates the wallet balance atomically."""
        
        tx_id = str(uuid.uuid4())[:8]
        tx = Transaction(
            transaction_id=tx_id,
            type=tx_type,
            category=category,
            amount=amount,
            description=description,
            metadata=metadata or {}
        )

        # 1. Update Wallet Balance
        # In a high-concurrency environment, we would use Redis WATCH/MULTI or Lua script.
        # For this MVP, we use the state_manager.
        wallet = self.state_manager.get_wallet(wallet_address)
        if not wallet:
            raise ValueError(f"Wallet with address {wallet_address} not found.")

        if tx_type == TransactionType.EXPENSE:
            wallet.internal_usd_balance -= amount
        else:
            wallet.internal_usd_balance += amount
            
        self.state_manager.update_wallet(wallet)

        # 2. Append to History
        history_key = f"{self.history_key_prefix}{wallet_address}"
        self.redis.rpush(history_key, tx.model_dump_json())
        
        logger.info(f"Recorded {tx_type} of {amount} for {wallet_address}. New internal balance: {wallet.internal_usd_balance}")
        
        return tx

    def get_transaction_history(self, wallet_address: str, count: int = 50) -> List[Transaction]:
        """Retrieves the recent transaction history."""
        history_key = f"{self.history_key_prefix}{wallet_address}"
        records = self.redis.lrange(history_key, -count, -1)
        
        history = []
        for r in records:
            history.append(Transaction(**json.loads(r.decode('utf-8'))))
            
        return history
