"""Diagnostic script to verify SMOS v2 environment and API access."""

import os
import sys
import logging
from typing import List
import google.genai as genai
from google.cloud import storage
import redis
from app.core.config import settings
from app.core.vertex_init import get_genai_client

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("SetupCheck")

def check_env_vars():
    """Checks if required environment variables are set."""
    required = ["PROJECT_ID", "LOCATION", "GCS_BUCKET_NAME", "APIFY_TOKEN"]
    missing = []
    for var in required:
        val = getattr(settings, var, None)
        if not val or "placeholder" in str(val):
            missing.append(var)
    
    if missing:
        logger.error(f"Missing or placeholder environment variables: {', '.join(missing)}")
        return False
    logger.info("SUCCESS: All required environment variables are present.")
    return True

def check_gcp_access():
    """Verifies GCP authentication and Vertex AI connectivity."""
    try:
        client = get_genai_client()
        # Test Gemini access with a simple request
        client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="Ping"
        )
        logger.info("SUCCESS: Vertex AI (Gemini) access verified.")
        
        # Test GCS access
        storage_client = storage.Client(project=settings.PROJECT_ID)
        bucket = storage_client.bucket(settings.GCS_BUCKET_NAME)
        if bucket.exists():
            logger.info(f"SUCCESS: GCS Bucket '{settings.GCS_BUCKET_NAME}' found and accessible.")
        else:
            logger.error(f"FAILURE: GCS Bucket '{settings.GCS_BUCKET_NAME}' not found.")
            return False
            
    except Exception as e:
        logger.error(f"FAILURE: GCP/Vertex AI access error: {e}")
        return False
    return True

def check_redis():
    """Verifies connection to the StateDB (Redis)."""
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, socket_timeout=5)
        r.ping()
        logger.info(f"SUCCESS: Redis connected at {settings.REDIS_HOST}:{settings.REDIS_PORT}.")
    except Exception as e:
        logger.error(f"FAILURE: Redis connection error: {e}")
        return False
    return True

def check_apify():
    """Verifies if Apify token is present (basic check)."""
    if settings.APIFY_TOKEN and len(settings.APIFY_TOKEN) > 10:
        logger.info("SUCCESS: Apify Token format looks valid.")
        return True
    logger.warning("CAUTION: Apify Token is missing or too short. TrendScout will fail.")
    return False

def run_diagnostic():
    print("=== SMOS v2 Pre-Flight Diagnostic ===")
    results = [
        check_env_vars(),
        check_gcp_access(),
        check_redis(),
        check_apify()
    ]
    
    if all(results):
        print("\nPASSED: System is ready for the first Muse.")
        sys.exit(0)
    else:
        print("\nFAILED: Please fix the errors above before launching.")
        sys.exit(1)

if __name__ == "__main__":
    run_diagnostic()
