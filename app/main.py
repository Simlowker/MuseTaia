"""Main entry point for SMOS CLI and System."""

import argparse
import sys
import asyncio
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agents.root_agent import RootAgent
from app.agents.genesis_agent import GenesisAgent
from app.agents.visual_virtuoso import VisualVirtuoso
from app.core.schemas.trend import IntentObject, TrendType
from app.core.schemas.genesis import MuseProposal, GenesisDNA
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings

# Global Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sovereign Muse OS (SMOS) v2")

# --- API MODELS ---
class GenesisRequest(BaseModel):
    proposal_id: str
    draft_dna: GenesisDNA
    image_data_b64: Optional[str] = None # Simulating preview image data

# --- API ENDPOINTS ---

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
    muse_id = request.draft_dna.identity.name.lower().replace(" ", "-")
    
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
