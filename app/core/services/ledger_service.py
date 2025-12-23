"""Service for managing the financial ledger and wallet operations."""

import json
import logging
import uuid
import redis
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

        # 1. Update Wallet Balance atomically using Redis WATCH
        wallet_key = f"smos:state:wallet:{wallet_address}"
        MAX_RETRIES = 5
        
        with self.redis.pipeline() as pipe:
            for attempt in range(MAX_RETRIES):
                try:
                    pipe.watch(wallet_key)
                    
                    # Get current wallet state
                    wallet_data = pipe.get(wallet_key)
                    if not wallet_data:
                        raise ValueError(f"Wallet with address {wallet_address} not found.")
                    
                    wallet = Wallet.model_validate_json(wallet_data)
                    
                    # Apply transaction
                    if tx_type == TransactionType.EXPENSE:
                        wallet.internal_usd_balance -= amount
                    else:
                        wallet.internal_usd_balance += amount
                    
                    # Transactional update
                    pipe.multi()
                    pipe.set(wallet_key, wallet.model_dump_json())
                    
                    # Append to history in the same transaction
                    history_key = f"{self.history_key_prefix}{wallet_address}"
                    pipe.rpush(history_key, tx.model_dump_json())
                    
                    pipe.execute()
                    break # Success
                except redis.WatchError:
                    # Target key changed, retry
                    if attempt == MAX_RETRIES - 1:
                        logger.error(f"LEDGER: Max retries ({MAX_RETRIES}) reached for wallet {wallet_address}. Aborting.")
                        raise RuntimeError(f"Failed to update wallet {wallet_address} after max retries due to concurrency.")
                    continue

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

    def allocate_proactive_budget(self, topic: str, estimated_roi: float) -> bool:
        """Dynamically allocates credits for a proactive trend based on ROI.
        
        Returns:
            bool: True if budget is allocated, False if ROI is too low.
        """
        MIN_ROI_THRESHOLD = 1.5 # 50% profit margin required
        
        if estimated_roi < MIN_ROI_THRESHOLD:
            logger.warning(f"FINANCE: Budget denied for '{topic}'. Estimated ROI {estimated_roi} is below threshold.")
            return False
            
        logger.info(f"FINANCE: Budget allocated for '{topic}'. Proceeding with autonomous production.")
        return True

