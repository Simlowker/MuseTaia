"""Schemas for Trend Analysis and Reporting."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CONTROVERSIAL = "controversial"

class RelevanceScore(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BLOCKED = "blocked"

class TrendReport(BaseModel):
    """Structured analysis of a specific trend or topic."""
    topic: str = Field(..., description="The main subject of the trend")
    summary: str = Field(..., description="Brief summary of what is happening")
    sentiment: Sentiment = Field(..., description="General sentiment of the trend")
    relevance: RelevanceScore = Field(..., description="Relevance to the Muse's persona")
    reasoning: str = Field(..., description="Why this relevance score was assigned")
    keywords: List[str] = Field(default_factory=list, description="Associated hashtags or keywords")
    source_links: List[str] = Field(default_factory=list, description="URLs used for grounding")
