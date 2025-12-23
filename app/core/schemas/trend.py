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

class TrendType(str, Enum):
    FASHION = "fashion"
    TECH = "tech"
    ART = "art"
    CULTURE = "culture"
    LIFESTYLE = "lifestyle"

class IntentObject(BaseModel):
    """Structured CLI-style intent generated from trend analysis."""
    command: str = Field(..., description="The system command to execute (e.g. 'produce_content')")
    trend_type: TrendType
    urgency: str = Field("low", description="Urgency level: low, medium, high")
    target_audience: str = Field("general", description="Primary audience segment")
    parameters: dict = Field(default_factory=dict, description="Additional CLI-style flags and values")
    raw_intent: str = Field(..., description="Original descriptive intent")

class TrendReport(BaseModel):
    """Structured analysis of a specific trend or topic."""
    topic: str = Field(..., description="The main subject of the trend")
    summary: str = Field(..., description="Brief summary of what is happening")
    sentiment: Sentiment = Field(..., description="General sentiment of the trend")
    relevance: RelevanceScore = Field(..., description="Relevance to the Muse's persona")
    reasoning: str = Field(..., description="Why this relevance score was assigned")
    intent: Optional[IntentObject] = Field(None, description="Standardized system intent if relevant")
    keywords: List[str] = Field(default_factory=list, description="Associated hashtags or keywords")
    source_links: List[str] = Field(default_factory=list, description="URLs used for grounding")

