"""Main entry point for SMOS CLI and System."""

import argparse
import sys
import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.root_agent import RootAgent
from app.agents.genesis_agent import GenesisAgent
from app.agents.visual_virtuoso import VisualVirtuoso
from app.agents.visual_agent import VisualAgent
from app.agents.finance_agent import CFOAgent
from app.core.schemas.trend import IntentObject, TrendType
from app.core.schemas.genesis import MuseProposal, GenesisDNA
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings
from app.core.redis_client import get_redis_client
from app.state.models import Mood

# Global Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sovereign Muse OS (SMOS) v2")

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# --- API MODELS ---
class GenesisRequest(BaseModel):
    proposal_id: str
    draft_dna: GenesisDNA
    image_data_b64: Optional[str] = None # Simulating preview image data

# --- API ENDPOINTS ---

@app.get("/")
async def root():
    """Root endpoint for system identification."""
    return {"message": "Welcome to SMOS v2 - Autonomous Muse Engine"}

@app.get("/health")
async def health():
    """Health check endpoint for GKE/Liveness probes."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/stream/muse-status")
async def stream_status(request: Request):
    """Server-Sent Events (SSE) endpoint for the high-observability vitrine."""
    redis_client = get_redis_client()
    pubsub = redis_client.pubsub()
    
    try:
        pubsub.subscribe("smos:events:vitrine")
    except Exception as e:
        logger.error(f"SSE: Failed to subscribe to Redis: {e}")
        raise HTTPException(status_code=500, detail="StateDB connection failed")

    async def event_generator():
        try:
            while True:
                # Check for disconnection
                if await request.is_disconnected():
                    logger.info("SSE: Client disconnected from vitrine stream.")
                    break
                
                # Get message with timeout to allow heartbeat
                message = pubsub.get_message(ignore_subscribe_none=True, timeout=1.0)
                if message:
                    yield f"data: {message['data'].decode('utf-8')}\n\n"
                else:
                    # Heartbeat to keep connection alive
                    yield ": heartbeat\n\n"
                
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            logger.info("SSE: Stream cancelled by server.")
        except Exception as e:
            logger.error(f"SSE: Stream error: {e}")
        finally:
            pubsub.unsubscribe("smos:events:vitrine")
            pubsub.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/muses/surprise-me", response_model=MuseProposal)
async def surprise_me():
    """Returns a random Muse concept and a preview prompt."""
    agent = GenesisAgent()
    try:
        proposal = agent.generate_random_concept()
        return proposal
    except Exception as e:
        logger.error(f"Genesis: Surprise Me failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/muses/genesis")
async def launch_genesis(request: GenesisRequest):
    """Automates GCS storage of face_master and dna.json for a new Muse."""
    assets = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)
    
    # 0. Sanitize Input
    import re
    muse_id = request.draft_dna.identity.name.lower()
    muse_id = re.sub(r'[^a-z0-9\-]', '-', muse_id) # Only allow alphanumeric and dashes
    muse_id = muse_id.strip('-')
    
    if not muse_id:
        raise HTTPException(status_code=400, detail="Invalid Muse Name")
    
    try:
        # 1. Store DNA
        dna_json = request.draft_dna.model_dump_json()
        assets.upload_dna(muse_id, dna_json)
        
        # 2. Materialize Identity (Real Imagen 3 Flow)
        logger.info(f"GENESIS: Materializing visual identity for {muse_id}...")
        visual_agent = VisualAgent()
        
        # We generate the master face based on the DNA description
        prompt = f"Official studio portrait of {request.draft_dna.identity.name}. {request.draft_dna.identity.bio}. High-fashion aesthetic, 8k resolution, signature look."
        face_bytes = visual_agent.generate_image(prompt=prompt, aspect_ratio="1:1")
        
        assets.upload_asset(f"muses/{muse_id}/face_master.png", face_bytes)
        
        logger.info(f"GENESIS: Muse '{muse_id}' materialized in GCS.")
        return {"status": "materialized", "muse_id": muse_id, "gcs_path": f"gs://{settings.GCS_BUCKET_NAME}/muses/{muse_id}/"}
        
    except Exception as e:
        logger.error(f"GENESIS: Failed to materialize Muse: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/internal/checkpoint-ready")
async def checkpoint_ready():
    """Signals that the agent is fully loaded and ready for GKE snapshotting (CRIU)."""
    # In a real scenario, we would check if memory usage is stable and DNA is indexed.
    return {"ready": True, "process_id": os.getpid(), "timestamp": datetime.now(timezone.utc)}

# --- AUTONOMOUS DAEMONS ---

async def trend_scout_daemon():
    """Background task that periodically scans for high-VVS trends."""
    from app.agents.trend_scout import TrendScout
    from app.core.workflow_engine import WorkflowEngine
    from app.core.finance.cost_calculator import CostCalculator
    
    scout = TrendScout()
    engine = WorkflowEngine()
    cfo = CFOAgent()
    calc = CostCalculator()
    
    logger.info("DAEMON: TrendScout sentinel active.")
    
    while True:
        try:
            # 1. Scan Niche (e.g. Virtual Fashion)
            insights = await scout.scan_niche(["digital couture", "virtual fashion"])
            
            # 2. Filter by threshold (VVS > 50.0)
            for insight in insights:
                if insight.vvs_score > scout.vvs_threshold:
                    logger.info(f"DAEMON: High-VVS Trend detected ({insight.vvs_score}): {insight.topic}")
                    
                    # 3. CFO GATE: Verify Solvency
                    subject_id = "muse-01"
                    est_cost = calc.estimate_video_cost("veo-3.1", 5.0)
                    
                    wallet = engine.ledger_service.state_manager.get_wallet(subject_id)
                    history = engine.ledger_service.get_transaction_history(subject_id)
                    
                    if not wallet:
                        logger.warning(f"DAEMON: No wallet for {subject_id}, skipping.")
                        continue

                    solvency = cfo.verify_solvency(wallet, history, est_cost)
                    
                    if not solvency.is_authorized:
                        logger.warning(f"DAEMON: Financial block for trend '{insight.topic}': {solvency.reasoning}")
                        continue

                    # 4. Trigger Production Loop
                    await engine.produce_video_content_async(
                        intent=insight.suggested_intent,
                        mood=Mood(), # Default neutral mood
                        subject_id=subject_id
                    )
                    
        except Exception as e:
            logger.error(f"DAEMON: TrendScout loop failed: {e}")
            
        await asyncio.sleep(3600) # Scan every hour

@app.on_event("startup")
async def startup_event():
    """Initializes the system and starts autonomous daemons."""
    
    # 1. Wait for Redis (Resilience)
    redis_client = get_redis_client()
    max_retries = 5
    for i in range(max_retries):
        try:
            if redis_client.ping():
                logger.info("SYSTEM: StateDB (Redis) connected successfully.")
                break
        except Exception:
            logger.warning(f"SYSTEM: Waiting for Redis... (Attempt {i+1}/{max_retries})")
            await asyncio.sleep(2)
    else:
        logger.error("SYSTEM: Critical failure: Could not connect to Redis. Daemons disabled.")
        return

    # 2. Start Daemons
    asyncio.create_task(trend_scout_daemon())



# --- CLI LOGIC ---

async def produce_content(topic: str):
    """Executes the full production flow via the WorkflowEngine."""
    from app.core.workflow_engine import WorkflowEngine
    
    print(f"--- SMOS: Initiating Production for topic: {topic} ---")
    engine = WorkflowEngine()
    
    try:
        # We use the Best-of-N strategy for high quality
        result = engine.produce_best_of_n_video(
            intent=topic,
            mood=Mood(), # Start with neutral mood
            subject_id="muse-01",
            n=3
        )
        print(f"--- SMOS: Production SUCCESS (Score: {result.get('quality_score'):.4f}) ---")
        print(f"Review Path: {result.get('review_path')}")
        print(f"Total Cost: {result.get('production_cost')} USD")
    except Exception as e:
        print(f"--- SMOS: Production FAILED: {e} ---")
        logger.error(f"CLI: Production failure: {e}")

def main():
    parser = argparse.ArgumentParser(description="Sovereign Muse OS CLI")
    subparsers = parser.add_subparsers(dest="command")
    produce_parser = subparsers.add_parser("produce", help="Trigger content production")
    produce_parser.add_argument("--intent", required=True, help="The topic or intent for production")
    args = parser.parse_args()
    if args.command == "produce":
        asyncio.run(produce_content(args.intent))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
