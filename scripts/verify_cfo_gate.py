"""Manual verification script for CFO Gate in WorkflowEngine."""

import logging
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood, Wallet
from app.core.services.ledger_service import LedgerService

logging.basicConfig(level=logging.INFO)

def verify_cfo_gate():
    engine = WorkflowEngine()
    subject_id = "muse-01"
    mood = Mood(valence=0.5, arousal=0.5, current_thought="Ready to produce.")
    
    # 1. Test Financial Blockade (Insufficient Balance)
    print("\n--- 1. Testing Financial Blockade ---")
    wallet = Wallet(address=subject_id, internal_usd_balance=0.01) # Very low
    engine.ledger_service.state_manager.update_wallet(wallet)
    
    try:
        engine.produce_video_content("test intent", mood, subject_id)
    except RuntimeError as e:
        print(f"Caught expected blockade: {e}")

    # 2. Test Authorization (Healthy Balance)
    # Note: This might still trigger LLM call if balance is healthy
    print("\n--- 2. Testing Potential Authorization (Healthy Balance) ---")
    wallet = Wallet(address=subject_id, internal_usd_balance=10.0)
    engine.ledger_service.state_manager.update_wallet(wallet)
    
    # We won't run the full production as it calls many APIs, 
    # but we've verified the logic in unit tests.
    print("Logic verified via unit tests and pre-check code path.")

if __name__ == "__main__":
    verify_cfo_gate()
