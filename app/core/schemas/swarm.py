"""Schemas for Swarm tasks and HITL proposals."""

from typing import List, Optional, Any, Dict
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.core.schemas.trend import IntentObject

class ProposalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"

class MissionProposal(BaseModel):
    """A proactive content proposal from the Muse waiting for human validation."""
    proposal_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: ProposalStatus = Field(default=ProposalStatus.PENDING)
    intent: IntentObject
    suggested_script: Optional[str] = None
    suggested_layout: Optional[Dict[str, Any]] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class PendingTask(BaseModel):
    """A task that is currently paused at a validation gate."""
    task_id: str
    agent_id: str
    step_name: str # e.g., 'pre-render-check'
    context_data: Dict[str, Any]
    preview_url: Optional[str] = None
