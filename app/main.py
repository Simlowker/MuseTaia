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
from app.core.schemas.trend import IntentObject, TrendType
from app.core.schemas.genesis import MuseProposal, GenesisDNA
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings
from app.core.redis_client import get_redis_client

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
        
        # 2. Store Face Master (Simulated from preview)
        # In a real flow, the front-end would send the confirmed image bytes
        # or we would trigger a formal generation here.
        assets.upload_asset(f"muses/{muse_id}/face_master.png", b"fake_face_master_bytes")
        
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
    
    scout = TrendScout()
    engine = WorkflowEngine()
    
    logger.info("DAEMON: TrendScout sentinel active.")
    
    while True:
        try:
            # 1. Scan Niche (e.g. Virtual Fashion)
            insights = await scout.scan_niche(["digital couture", "virtual fashion"])
            
            # 2. Filter by threshold (VVS > 50.0)
            for insight in insights:
                if insight.vvs_score > scout.vvs_threshold:
                    logger.info(f"DAEMON: High-VVS Trend detected ({insight.vvs_score}): {insight.topic}")
                    # 3. Trigger Production Loop
                    await engine.produce_video_content_async(
                        intent=insight.suggested_intent,
                        mood=Mood(), # Default neutral mood
                        subject_id="muse-01"
                    )
                    
        except Exception as e:
            logger.error(f"DAEMON: TrendScout loop failed: {e}")
            
        await asyncio.sleep(3600) # Scan every hour

@app.on_event("startup")
async def startup_event():
    """Starts autonomous daemons on server startup."""
    asyncio.create_task(trend_scout_daemon())



# --- CLI LOGIC ---

async def produce_content(topic: str):
    """Simulates the full production flow via the Lobe architecture."""
    print(f"--- SMOS: Initiating Production for topic: {topic} ---")
    root = RootAgent()
    intent = IntentObject(
        command="produce_content",
        trend_type=TrendType.FASHION,
        urgency="medium",
        target_audience="creatives",
        raw_intent=f"High-fashion digital piece about {topic}",
        parameters={}
    )
    print("Brain Lobe: Planning execution graph...")
    task_graph = root.execute_intent(intent)
    for node in task_graph.nodes:
        print(f"Executing Node: {node.agent_id} ({node.agent_type}) - {node.instruction}")
    print("--- SMOS: Production Intent Processed Successfully ---")

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
