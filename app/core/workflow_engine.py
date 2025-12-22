"""Core engine for executing multi-agent workflows with QA loops."""

import logging
from typing import Optional, Dict, Any
from app.agents.narrative_agent import NarrativeAgent
from app.agents.visual_agent import VisualAgent
from app.agents.critic_agent import CriticAgent
from typing import Optional, Dict, Any, List
import io
from PIL import Image, ImageDraw
from app.agents.narrative_agent import NarrativeAgent
from app.agents.visual_agent import VisualAgent
from app.agents.critic_agent import CriticAgent
from app.agents.director_agent import DirectorAgent
from app.agents.eic_agent import EICAgent
from app.core.utils.prompt_optimizer import PromptOptimizer
from app.state.models import Mood
from app.matrix.assets_manager import SignatureAssetsManager
from app.core.config import settings

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Orchestrates the execution of agent tasks with integrated QA loops."""

    def __init__(self):
        self.narrative_agent = NarrativeAgent()
        self.visual_agent = VisualAgent()
        self.critic_agent = CriticAgent()
        self.director_agent = DirectorAgent()
        self.eic_agent = EICAgent()
        self.optimizer = PromptOptimizer()
        self.assets_manager = SignatureAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)

    def _create_mask_from_bbox(self, base_image_bytes: bytes, bbox_2d: List[int]) -> bytes:
        """Creates a binary mask image from a bounding box."""
        with Image.open(io.BytesIO(base_image_bytes)) as img:
            mask = Image.new("L", img.size, 0) # Black background
            draw = ImageDraw.Draw(mask)
            
            # bbox_2d is [ymin, xmin, ymax, xmax] normalized 0-1000
            width, height = img.size
            ymin, xmin, ymax, xmax = bbox_2d
            
            # Convert normalized coords to pixels
            coords = [
                xmin * width / 1000,
                ymin * height / 1000,
                xmax * width / 1000,
                ymax * height / 1000
            ]
            
            draw.rectangle(coords, fill=255) # White target area
            
            output = io.BytesIO()
            mask.save(output, format="PNG")
            return output.getvalue()

    def produce_video_content(
        self, 
        intent: str, 
        mood: Mood, 
        subject_id: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Runs the full production pipeline with visual QA.
        
        Sequence: Narrative -> Optimize -> Visual -> Critic (Loop) -> Director -> EIC (Staging).
        """
        
        # 1. Narrative Phase
        logger.info("Starting Narrative Phase...")
        script_data = self.narrative_agent.generate_content(intent, mood)
        
        # 2. Optimization Phase
        logger.info("Optimizing prompt...")
        optimized_prompt = self.optimizer.optimize(script_data.script)
        
        # 3. Visual & QA Loop
        logger.info("Starting Visual & QA Loop...")
        reference_image = self.assets_manager.download_asset(f"muses/{subject_id}/face.png")
        
        current_image = self.visual_agent.generate_image(optimized_prompt, subject_id=subject_id)
        
        for attempt in range(max_retries):
            # QA check
            report = self.critic_agent.verify_consistency(reference_image, current_image)
            
            if report.is_consistent:
                logger.info("Visual consistency verified by The Critic.")
                break
            
            logger.warning(f"The Critic rejected asset. Attempt {attempt+1}/{max_retries}")
            
            # Check for actionable feedback (Repair vs Regenerate)
            repaired = False
            if report.feedback:
                item = report.feedback[0] # Handle highest priority
                if item.action_type == "inpaint" and item.target_area:
                    logger.info(f"Attempting repair: Inpainting {item.target_area}")
                    
                    # 1. Detect Mask
                    bbox = self.critic_agent.detect_mask_area(current_image, item.target_area)
                    if bbox:
                        mask_bytes = self._create_mask_from_bbox(current_image, bbox)
                        # 2. Inpaint
                        current_image = self.visual_agent.edit_image(
                            prompt=f"Fix {item.target_area}. {item.description}",
                            base_image_bytes=current_image,
                            mask_image_bytes=mask_bytes
                        )
                        repaired = True
            
            if not repaired:
                # Fallback to full regeneration if no specific repair possible
                logger.info("Fallback: Full regeneration.")
                current_image = self.visual_agent.generate_image(optimized_prompt, subject_id=subject_id)
        
        final_image = current_image
            
        # 4. Production Phase
        logger.info("Starting Cinematography Phase...")
        video_data = self.director_agent.generate_video(optimized_prompt, image_bytes=final_image)
        
        production_data = {
            "title": script_data.title,
            "caption": script_data.caption,
            "video_bytes": video_data,
            "poster_image_bytes": final_image
        }

        # 5. Staging Phase (EIC)
        logger.info("Staging for review...")
        review_path = self.eic_agent.stage_for_review(production_data, subject_id)
        
        production_data["review_path"] = review_path
        return production_data
