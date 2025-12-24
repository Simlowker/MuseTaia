
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.core.schemas.trend import TrendReport, ViralVelocity, Sentiment, RelevanceScore, TrendType
from app.state.models import Mood, Wallet
from app.core.redis_client import get_redis_client
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

# --- ROUTERS ---
perception = APIRouter(prefix="/perception", tags=["Perception"])
state = APIRouter(prefix="/state", tags=["State"])
finance = APIRouter(prefix="/finance", tags=["Finance"])
swarm = APIRouter(prefix="/swarm", tags=["Swarm"])
studio = APIRouter(prefix="/studio", tags=["Studio"])
hitl = APIRouter(prefix="/hitl", tags=["HITL"])

# --- MOCK DATA GENERATORS (Fallback) ---
def get_mock_trends() -> List[TrendReport]:
    return [
        TrendReport(
            topic="Digital Couture",
            summary="Rise of purely digital fashion assets in AR spaces.",
            sentiment=Sentiment.POSITIVE,
            relevance=RelevanceScore.HIGH,
            reasoning="Perfect fit for virtual Muse persona.",
            vvs=ViralVelocity(score=8.5, acceleration="Rising", engagement_rate=120.5),
            estimated_roi=4.2,
            keywords=["#digitalfashion", "#metaverse", "#ar"],
            trend_type=TrendType.FASHION
        ),
         TrendReport(
            topic="Neo-Brutalism UI",
            summary="Return to raw, unpolished aesthetics in digital design.",
            sentiment=Sentiment.NEUTRAL,
            relevance=RelevanceScore.MEDIUM,
            reasoning="Aligns with current system aesthetic but niche.",
            vvs=ViralVelocity(score=6.2, acceleration="Stagnant", engagement_rate=45.0),
            estimated_roi=2.1,
            keywords=["#ui", "#design", "#brutalism"],
            trend_type=TrendType.TECH
        )
    ]

# --- PERCEPTION ENDPOINTS ---
@perception.get("/trends/active", response_model=List[TrendReport])
async def get_active_trends():
    """Returns currently tracked high-VVS trends."""
    # In a real scenario, this would fetch from Redis/Vector DB
    # For now, we return mock data to unblock frontend
    return get_mock_trends()

@perception.get("/signals/queue")
async def get_signals_queue():
    """Returns raw signals waiting for processing."""
    return []

# --- STATE ENDPOINTS ---
@state.get("/mood", response_model=Mood)
async def get_mood():
    """Returns the current emotional state of the Muse."""
    redis = get_redis_client()
    try:
        data = redis.get(f"smos:{settings.PROJECT_ID}:mood")
        if data:
            return Mood.model_validate_json(data)
    except Exception as e:
        logger.warning(f"Failed to fetch mood from Redis: {e}")
    
    return Mood(current_thought="System initializing...", valence=0.1, arousal=0.5, dominance=0.8)

# --- FINANCE ENDPOINTS ---
@finance.get("/wallet", response_model=Wallet)
async def get_wallet():
    """Returns the genesis wallet state."""
    # Mocking for now as wallet might not be initialized in Redis
    return Wallet(
        address="genesis-vault-01", 
        balance=124.50, 
        currency="SOL", 
        internal_usd_balance=5000.00,
        daily_spend=12.50,
        daily_budget=100.00
    )

@finance.get("/ledger/{address}")
async def get_ledger(address: str):
    return []

# --- SWARM ENDPOINTS ---
@swarm.get("/status")
async def get_swarm_status():
    return [
        {"id": "trend-scout", "status": "active", "task": "Scanning TikTok"},
        {"id": "cfo-agent", "status": "idle", "task": "Monitoring"},
        {"id": "visual-agent", "status": "standby", "task": "Awaiting Production"}
    ]

@swarm.get("/pipeline")
async def get_pipeline():
    return {"active_productions": 0, "queue_depth": 0}

# --- STUDIO ENDPOINTS ---
@studio.get("/productions/active")
async def get_active_productions():
    return []

@studio.get("/productions/history")
async def get_production_history():
    return []

# --- HITL ENDPOINTS ---
@hitl.get("/proposals")
async def get_proposals():
    return []
