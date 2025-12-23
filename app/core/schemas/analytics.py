"""Schemas for performance analytics and learning loops."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class PerformanceMetrics(BaseModel):
    """Real-world analytics for a published post."""
    post_id: str
    views: int = 0
    likes: int = 0
    shares: int = 0
    retention_rate: float = 0.0 # 0.0 to 1.0
    cpm_realized: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PostMortem(BaseModel):
    """Synthesized lessons from a production cycle."""
    task_id: str
    original_vvs: float
    actual_performance: PerformanceMetrics
    success_factors: List[str]
    failure_factors: List[str]
    pattern_updates: Dict[str, Any]
    next_step_strategy: str
