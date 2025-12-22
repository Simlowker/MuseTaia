"""Editor-in-Chief (EIC) agent for staging and final routing of content."""

import logging
from typing import Dict, Any
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings

logger = logging.getLogger(__name__)

class EICAgent:
    """The Editor-in-Chief agent responsible for final curation and staging."""

    def __init__(self):
        self.assets_manager = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)

    def stage_for_review(self, production_data: Dict[str, Any], subject_id: str) -> str:
        """Stages the generated assets in a specific review folder in GCS.
        
        Args:
            production_data: Dict containing video_bytes, poster_image_bytes, title, caption.
            subject_id: The ID of the Muse.
            
        Returns:
            str: The base GCS path where assets are staged.
        """
        import uuid
        review_id = str(uuid.uuid4())[:8]
        base_path = f"reviews/{subject_id}/{review_id}"
        
        logger.info(f"Staging content for review: {base_path}")
        
        # 1. Upload Video
        video_path = f"{base_path}/video.mp4"
        self.assets_manager.upload_asset(
            video_path, 
            production_data["video_bytes"],
            metadata={"title": production_data["title"], "type": "final_video"}
        )
        
        # 2. Upload Poster Image
        poster_path = f"{base_path}/poster.png"
        self.assets_manager.upload_asset(
            poster_path, 
            production_data["poster_image_bytes"],
            metadata={"type": "final_poster"}
        )
        
        # 3. Upload Metadata (Caption/Title)
        import json
        meta_data = {
            "title": production_data["title"],
            "caption": production_data["caption"]
        }
        self.assets_manager.upload_asset(
            f"{base_path}/metadata.json",
            json.dumps(meta_data).encode("utf-8"),
            metadata={"type": "review_metadata"}
        )
        
        return base_path
