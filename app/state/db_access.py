"""Database access layer for the Muse's shared state."""

import json
from datetime import datetime, timezone
from typing import Optional
from app.core.redis_client import get_redis_client
from app.state.models import Mood, Wallet

class StateManager:
    """Manages read/write access to the application state in Redis."""

    def __init__(self):
        self.redis = get_redis_client()
        self.mood_key = "smos:state:mood"
        self.wallet_key_prefix = "smos:state:wallet:"

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
