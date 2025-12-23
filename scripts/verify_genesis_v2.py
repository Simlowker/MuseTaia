"""Manual verification script for Genesis Pipeline & Studio Automation."""

import requests
import json

def verify_genesis_flow():
    print("--- 1. Testing /muses/surprise-me ---")
    # This assumes the server is running (e.g. via uvicorn app.main:app)
    # If not running, we'll just verify the logic locally via agents.
    from app.agents.genesis_agent import GenesisAgent
    agent = GenesisAgent()
    
    try:
        proposal = agent.generate_random_concept()
        print(f"Random Muse Generated: {proposal.draft_dna.identity.name}")
        print(f"Concept: {proposal.concept_summary}")
        print(f"Preview Prompt: {proposal.preview_prompt}")
        
        print("\n--- 2. Testing Genesis Materialization (GCS Logic) ---")
        from app.matrix.assets_manager import SignatureAssetsManager
        from app.core.config import settings
        
        assets = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)
        muse_id = proposal.draft_dna.identity.name.lower().replace(" ", "-")
        
        # Test automated storage
        dna_json = proposal.draft_dna.model_dump_json()
        assets.upload_dna(muse_id, dna_json)
        assets.upload_asset(f"muses/{muse_id}/face_master.png", b"fake_face_master_bytes")
        
        print(f"SUCCESS: Muse '{muse_id}' assets materialized in GCS.")
        
    except Exception as e:
        print(f"Genesis verification failed: {e}")

if __name__ == "__main__":
    verify_genesis_flow()
