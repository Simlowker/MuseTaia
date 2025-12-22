"""Data models for the Muse's shared state."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class Mood(BaseModel):
    """Represents the emotional state of the Muse."""
    valence: float = Field(0.0, ge=-1.0, le=1.0, description="Positivity vs Negativity")
    arousal: float = Field(0.0, ge=0.0, le=1.0, description="Excitement vs Calm")
    dominance: float = Field(0.0, ge=0.0, le=1.0, description="Control vs Submission")
    current_thought: Optional[str] = Field(None, description="Current internal monologue")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Wallet(BaseModel):
    """Represents the financial state of the Muse."""
    address: str = Field(..., description="Wallet address")
    balance: float = Field(0.0, ge=0.0, description="Current balance")
    currency: str = Field("SOL", description="Currency symbol")
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
