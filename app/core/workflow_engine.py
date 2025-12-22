"""Core engine for executing multi-agent workflows with QA loops."""

import logging
from typing import Optional, Dict, Any
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
        
        final_image = None
        for attempt in range(max_retries):
            logger.info(f"Visual generation attempt {attempt + 1}")
            candidate_image = self.visual_agent.generate_image(optimized_prompt, subject_id=subject_id)
            
            # QA check
            report = self.critic_agent.verify_consistency(reference_image, candidate_image)
            if report.is_consistent:
                logger.info("Visual consistency verified by The Critic.")
                final_image = candidate_image
                break
            else:
                logger.warning(f"The Critic rejected asset: {report.issues}")
        
        if not final_image:
            raise RuntimeError(f"Failed to produce consistent visual after {max_retries} attempts.")
            
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
