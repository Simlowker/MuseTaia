"""Schemas for Market Intelligence and Trend Discovery."""

from pydantic import BaseModel, Field
from typing import List, Optional

class TrendInsight(BaseModel):
    """Normalized and filtered market signal."""
    trend_fingerprint: str = Field(..., description="Unique hash for deduplication")
    topic: str
    vvs_score: float = Field(..., description="Viral Velocity Score (VVS)")
    platform: str # 'reddit', 'tiktok', etc.
    sentiment_index: float = Field(0.0, description="Sentiment index from -1.0 to 1.0")
    visual_context_urls: List[str] = Field(default_factory=list)
    suggested_intent: str = Field(..., description="Suggested CLI command for the RootAgent")
