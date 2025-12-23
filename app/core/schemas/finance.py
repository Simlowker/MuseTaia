"""Schemas for financial transactions and economic events."""

from typing import List, Optional
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(str, Enum):
    SPONSORSHIP = "sponsorship"
    API_COST = "api_cost"
    STORAGE_COST = "storage_cost"
    COMMUNITY_GRANT = "community_grant"
    OTHER = "other"

class Transaction(BaseModel):
    """Represents a single financial record."""
    transaction_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    type: TransactionType
    category: TransactionCategory
    amount: float = Field(..., gt=0)
    currency: str = Field("USD", description="Currency for cost tracking (internal unit)")
    description: str
    metadata: Optional[dict] = Field(default_factory=dict)

class SolvencyCheck(BaseModel):
    """Result of the imperative solvency verification."""
    is_authorized: bool = Field(..., description="Is the action financially authorized?")
    projected_balance: float
    reasoning: str = Field(..., description="Justification based on Hard Constraints")
    circuit_breaker_active: bool = False

class LedgerHistory(BaseModel):
    """Represents the financial history of the Muse."""
    transactions: List[Transaction] = Field(default_factory=list)
