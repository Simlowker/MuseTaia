"""Automated visual regression test runner for SMOS identity anchors."""

import sys
import logging
import asyncio
from typing import Dict, Any
from app.agents.visual_agent import VisualAgent
from app.core.utils.visual_comparison import VisualComparator
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Thresholds
MIN_SIMILARITY_SCORE = 0.90 # High level identity
MAX_PIXEL_DEVIATION = 0.05  # SSIM/RMSE proxy (1.0 - score)

async def run_regression(muse_id: str = "genesis"):
    """Triggers a render and compares it against the Genesis anchor."""
    
    logger.info(f"Starting visual regression test for Muse: {muse_id}")
    
    visual_agent = VisualAgent()
    comparator = VisualComparator()
    assets_manager = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)
    
    # 1. Fetch Identity Anchor
    anchor_path = f"muses/{muse_id}/anchors/face_front.png"
    try:
        anchor_bytes = assets_manager.download_asset(anchor_path)
    except Exception:
        logger.error(f"Genesis anchor not found at {anchor_path}. Please register anchors first.")
        sys.exit(1)
        
    # 2. Trigger Test Render
    logger.info("Generating test render...")
    test_prompt = "A high-quality portrait of the muse, neutral expression, soft lighting."
    render_bytes = visual_agent.generate_image(test_prompt, subject_id=muse_id)
    
    # 3. Compare Identity
    logger.info("Performing identity analysis...")
    id_result = comparator.compare_identity(anchor_bytes, render_bytes)
    
    # 4. Compare Pixels
    pixel_score = comparator.calculate_pixel_similarity(anchor_bytes, render_bytes)
    
    # --- LOG RESULTS ---
    logger.info(f"Similarity Score: {id_result.similarity_score}")
    logger.info(f"Identity Match: {id_result.identity_match}")
    logger.info(f"Pixel Similarity: {pixel_score}")
    
    # --- ENFORCE THRESHOLDS ---
    failed = False
    if not id_result.identity_match:
        logger.error(f"FAILURE: Identity mismatch detected! Details: {id_result.deviation_details}")
        failed = True
        
    if id_result.similarity_score < MIN_SIMILARITY_SCORE:
        logger.error(f"FAILURE: Similarity score {id_result.similarity_score} below threshold {MIN_SIMILARITY_SCORE}")
        failed = True
        
    # Note: Pixel deviation rule (2%)
    deviation = 1.0 - pixel_score
    if deviation > 0.02:
        logger.warning(f"CAUTION: Pixel deviation is {deviation:.2%}, exceeding 2% target.")
        # We don't fail the build on pixel deviation alone for now, just warn.
        
    if failed:
        logger.error("Visual regression test FAILED.")
        sys.exit(1)
    else:
        logger.info("Visual regression test PASSED. Identity is consistent.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        muse_id = sys.argv[1]
    else:
        muse_id = "genesis"
        
    asyncio.run(run_regression(muse_id))
