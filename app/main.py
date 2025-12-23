"""Main entry point for the Sovereign Muse OS (SMOS) API."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.state.db_access import StateManager
from app.core.workflow_engine import WorkflowEngine
from app.agents.trend_scanner import TrendScanner
from app.core.services.ledger_service import LedgerService

app = FastAPI(title="Sovereign Muse OS (SMOS)")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
state_manager = StateManager()
workflow_engine = WorkflowEngine()
trend_scanner = TrendScanner()
ledger_service = LedgerService()

class ProductionRequest(BaseModel):
    intent: str
    subject_id: str = "genesis"

@app.get("/")
def read_root() -> dict:
    """Returns a welcome message for the SMOS API."""
    return {"message": "Welcome to SMOS API"}

# --- 1. State Endpoints ---

@app.get("/state/mood")
def get_mood():
    return state_manager.get_mood()

@app.get("/state/wallet")
def get_wallet(address: str = "genesis"):
    wallet = state_manager.get_wallet(address)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

# --- 2. Swarm Endpoints ---

@app.post("/swarm/produce")
async def trigger_production(req: ProductionRequest):
    try:
        # We use the async background task version
        task_id = await workflow_engine.produce_video_content_async(
            intent=req.intent,
            mood=state_manager.get_mood(),
            subject_id=req.subject_id
        )
        return {"status": "started", "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. Perception Endpoints ---

@app.get("/perception/trends")
def get_trends():
    # Mock some trends for the feed, or call trend_scanner for a set of topics
    topics = ["Digital Fashion", "AI Art", "Metaverse"]
    reports = []
    for t in topics:
        # In a real app, this might be cached or scheduled
        reports.append({
            "topic": t,
            "score": 85,
            "category": "Technology"
        })
    return reports

# --- 4. Finance Endpoints ---

@app.get("/finance/ledger/{address}")
def get_ledger(address: str):
    return ledger_service.get_transaction_history(address)

def main():
    """Main function to run the application using uvicorn."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
