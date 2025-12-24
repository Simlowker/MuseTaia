"""System bootstrap script to initialize SMOS state and verify connectivity."""

import os
import sys
import logging
from app.state.db_access import StateManager
from app.state.models import Mood, Wallet
from app.core.config import settings

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def bootstrap():
    logger.info("Initializing Sovereign Muse OS (SMOS)...")
    
    # 1. Verify Config
    if settings.PROJECT_ID == "placeholder-project-id":
        logger.warning("Warning: PROJECT_ID is still set to placeholder. Please check your .env file.")
    
    # 2. Initialize StateDB (Redis)
    try:
        sm = StateManager()
        
        # Initialize Mood
        logger.info("Setting initial MoodState...")
        initial_mood = Mood(
            valence=0.5, 
            arousal=0.5, 
            dominance=0.8, 
            current_thought="System initialized. Awaiting human or community direction."
        )
        sm.update_mood(initial_mood)
        
        # Initialize Wallet
        logger.info("Initializing Genesis Wallet...")
        initial_wallet = Wallet(
            address="genesis",
            balance=1.0,
            currency="SOL",
            internal_usd_balance=100.0 # Starter budget for API calls
        )
        sm.update_wallet(initial_wallet)
        
        logger.info("SUCCESS: StateDB initialized.")
        
    except Exception as e:
        logger.error(f"FAILURE: Could not connect to Redis: {e}")
        sys.exit(1)

    # 3. Verify GCP Connectivity (Simple checks)
    logger.info("Checking Google Cloud Storage access...")
    try:
        from google.cloud import storage
        # Explicitly pass project to avoid ADC warning/error if env var is missing
        client = storage.Client(project=settings.PROJECT_ID)
        buckets = list(client.list_buckets(max_results=1))
        logger.info(f"SUCCESS: GCP Storage access verified for project '{settings.PROJECT_ID}'.")
    except Exception as e:
        logger.warning(f"CAUTION: GCP Storage check failed: {e}")

    logger.info("Bootstrap complete. System is ready for backend launch.")

if __name__ == "__main__":
    bootstrap()
