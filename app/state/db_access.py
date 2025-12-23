"""Database access layer for the Muse's shared state."""

import json
from datetime import datetime, timezone
from typing import Optional, List, Any
from app.core.redis_client import get_redis_client
from app.state.models import Mood, Wallet
from app.core.schemas.swarm import MissionProposal, PendingTask

class StateManager:
    """Manages read/write access to the application state in Redis."""

    def __init__(self):
        self.redis = get_redis_client()
        self.mood_key = "smos:state:mood"
        self.wallet_key_prefix = "smos:state:wallet:"
        self.proposal_key = "smos:swarm:proposals"
        self.pending_tasks_key = "smos:swarm:pending"

    def get_mood(self) -> Mood:
        """Retrieves the current mood."""
        data = self.redis.get(self.mood_key)
        if not data:
            return Mood()
        
        # Decode bytes to string then load JSON
        json_data = json.loads(data.decode('utf-8'))
        return Mood(**json_data)

    def update_mood(self, mood: Mood) -> None:
        """Updates the current mood."""
        mood.last_updated = datetime.now(timezone.utc)
        self.redis.set(self.mood_key, mood.model_dump_json())

    def get_wallet(self, address: str) -> Optional[Wallet]:
        """Retrieves wallet information for a given address."""
        key = f"{self.wallet_key_prefix}{address}"
        data = self.redis.get(key)
        if not data:
            return None
        
        json_data = json.loads(data.decode('utf-8'))
        return Wallet(**json_data)

    def update_wallet(self, wallet: Wallet) -> None:
        """Updates the wallet state."""
        key = f"{self.wallet_key_prefix}{wallet.address}"
        wallet.last_updated = datetime.now(timezone.utc)
        self.redis.set(key, wallet.model_dump_json())

    # --- HITL & Swarm Persistence ---

    def add_proposal(self, proposal: MissionProposal) -> None:
        """Adds a new proactive proposal to the queue."""
        self.redis.rpush(self.proposal_key, proposal.model_dump_json())

    def get_proposals(self, count: int = 10) -> List[MissionProposal]:
        """Retrieves the latest proposals."""
        records = self.redis.lrange(self.proposal_key, -count, -1)
        return [MissionProposal(**json.loads(r.decode('utf-8'))) for r in records]

    def set_pending_task(self, task: PendingTask) -> None:
        """Stores a task that is currently suspended for HITL."""
        self.redis.hset(self.pending_tasks_key, task.task_id, task.model_dump_json())

    def get_pending_task(self, task_id: str) -> Optional[PendingTask]:
        """Retrieves a pending task by ID."""
        data = self.redis.hget(self.pending_tasks_key, task_id)
        if not data:
            return None
        return PendingTask(**json.loads(data.decode('utf-8')))

    def remove_pending_task(self, task_id: str) -> None:
        """Clears a task from the pending set after resolution."""
        self.redis.hdel(self.pending_tasks_key, task_id)

