"""Core engine for executing multi-agent workflows with QA loops."""

import logging
import io
from typing import Optional, Dict, Any, List
from PIL import Image, ImageDraw

from app.agents.narrative_agent import NarrativeAgent
from app.agents.visual_agent import VisualAgent
from app.agents.critic_agent import CriticAgent
from app.agents.director_agent import DirectorAgent
from app.agents.eic_agent import EICAgent
from app.agents.architect_agent import ArchitectAgent
from app.agents.stylist_agent import StylistAgent
from app.core.utils.prompt_optimizer import PromptOptimizer
from app.state.models import Mood
from app.matrix.world_dna import WorldRegistry
from app.matrix.world_assets import WorldAssetsManager
from app.matrix.wardrobe_dna import WardrobeRegistry
from app.matrix.wardrobe_assets import WardrobeAssetsManager
from app.core.config import settings
from app.core.services.ledger_service import LedgerService
from app.core.finance.cost_calculator import CostCalculator
from app.core.schemas.finance import TransactionType, TransactionCategory
from app.core.services.comfy_api import ComfyUIClient
from app.core.schemas.swarm import PendingTask

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Orchestrates the execution of agent tasks with integrated QA loops."""

    def __init__(self):
        self.narrative_agent = NarrativeAgent()
        self.visual_agent = VisualAgent()
        self.critic_agent = CriticAgent()
        self.director_agent = DirectorAgent()
        self.eic_agent = EICAgent()
        self.architect_agent = ArchitectAgent()
        self.stylist_agent = StylistAgent()
        
        self.optimizer = PromptOptimizer()
        self.world_registry = WorldRegistry()
        self.world_assets = WorldAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)
        
        self.wardrobe_registry = WardrobeRegistry()
        self.wardrobe_assets = WardrobeAssetsManager(bucket_name=settings.GCS_BUCKET_NAME)
        
        self.ledger_service = LedgerService()
        self.cost_calculator = CostCalculator()
        self.comfy_client = ComfyUIClient()

    def _render_via_comfy(self, prompt: str, reference_images: List[bytes]) -> bytes:
        """Executes a high-fidelity render via ComfyUI nodal workflow."""
        logger.info("COMFY_UI: Triggering nodal workflow render...")
        # Conceptual workflow JSON
        workflow = {
            "3": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["3", 1]}},
            # ... more nodes for Imagen 3 / Veo 3.1 wrappers ...
        }
        prompt_id = self.comfy_client.queue_prompt(workflow)
        return self.comfy_client.get_output_data(prompt_id) or b""

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

    def _wait_for_approval(self, task_id: str, step_name: str, context: Dict[str, Any], preview_data: Optional[bytes] = None) -> bool:
        """Suspends execution and waits for a human approval signal in Redis."""
        import time
        logger.info(f"HITL_GATE: Pausing at '{step_name}'. Waiting for master signal...")
        
        # 1. Register Pending Task
        task = PendingTask(
            task_id=task_id,
            agent_id="orchestrator",
            step_name=step_name,
            context_data=context
        )
        self.ledger_service.state_manager.set_pending_task(task)
        
        # 2. Polling Loop (In a real system, we'd use Pub/Sub or a long-poll)
        # For MVP, we poll Redis for a specific approval key
        approval_key = f"smos:swarm:approve:{task_id}"
        timeout = 300 # 5 minutes max wait
        start_time = time.time()
        
        try:
            while time.time() - start_time < timeout:
                approval = self.ledger_service.redis.get(approval_key)
                if approval:
                    action = approval.decode('utf-8')
                    if action == "approve":
                        logger.info(f"HITL_GATE: Received APPROVAL for {task_id}")
                        return True
                    elif action == "reject":
                        logger.info(f"HITL_GATE: Received REJECTION for {task_id}")
                        return False
                time.sleep(2)
        finally:
            self.ledger_service.state_manager.remove_pending_task(task_id)
            self.ledger_service.redis.delete(approval_key)
            
        logger.warning(f"HITL_GATE: Timeout waiting for approval on {task_id}")
        return False

    def produce_video_content(
        self, 
        intent: str, 
        mood: Mood, 
        subject_id: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Runs the full production pipeline with visual, spatial, and look QA."""
        
        # Determine mode from global state (importing from main is tricky, so we check Redis or a config)
        # For now, let's assume we fetch it from Redis
        is_sovereign = True
        mode_data = self.ledger_service.redis.get("smos:config:sovereign_mode")
        if mode_data:
            is_sovereign = mode_data.decode('utf-8') == "true"

        # 0. Budget Check
        logger.info("Checking production budget...")
        wallet = self.ledger_service.state_manager.get_wallet(subject_id)
        MIN_PRODUCTION_COST = 0.15
        if not wallet or wallet.internal_usd_balance < MIN_PRODUCTION_COST:
            current_bal = wallet.internal_usd_balance if wallet else 0
            raise RuntimeError(f"Insufficient budget for production. Required: {MIN_PRODUCTION_COST}, Current: {current_bal}")

        # Task ID for HITL tracking
        import uuid
        task_id = str(uuid.uuid4())[:8]

        # 1. Narrative Phase
        logger.info("Starting Narrative Phase...")
        script_data = self.narrative_agent.generate_content(intent, mood)
        
        # 2. Architectural Phase (World Engine)
        logger.info("Planning scene layout...")
        layout = self.architect_agent.plan_scene_layout(script_data.script, self.world_registry)
        
        # --- HITL GATE 1: SCRIPT & LAYOUT VALIDATION ---
        if not is_sovereign:
            approved = self._wait_for_approval(task_id, "script_validation", {
                "title": script_data.title, "script": script_data.script, "location": layout.location_id
            })
            if not approved:
                raise RuntimeError("Mission rejected by human master during script validation.")

        # 3. Stylist Phase (Look & Continuity)
        logger.info("Selecting wardrobe and props...")
        look = self.stylist_agent.select_look(script_data.script, layout, mood, self.wardrobe_registry)
        
        # 4. Optimization Phase
        logger.info("Optimizing prompt...")
        optimized_prompt = self.optimizer.optimize(
            f"{script_data.script}. Setting: {layout.scene_description}. Look: {look.visual_details}"
        )
        
        # 5. Visual & QA Loop
        logger.info("Starting Visual & QA Loop...")
        
        # Collect ALL reference assets (Identity + World + Look)
        references = []
        subject_face = self.world_assets.download_asset(f"muses/{subject_id}/face.png")
        references.append(subject_face)
        
        try:
            location_ref = self.world_assets.download_asset(f"world/locations/{layout.location_id}/reference.png")
            references.append(location_ref)
        except Exception: pass

        for obj_id in layout.selected_objects:
            try:
                obj_ref = self.world_assets.download_asset(f"world/objects/{obj_id}/reference.png")
                references.append(obj_ref)
            except Exception: pass
        
        for item_id in look.item_ids:
            try:
                item_ref = self.wardrobe_assets.download_asset(f"wardrobe/items/{item_id}/reference.png")
                references.append(item_ref)
            except Exception: pass

        current_image = self.visual_agent.generate_image(
            optimized_prompt, 
            subject_id=subject_id,
            location_id=layout.location_id,
            object_ids=layout.selected_objects,
            item_ids=look.item_ids
        )
        
        for attempt in range(max_retries):
            # Surgical QA check
            report = self.critic_agent.verify_consistency(current_image, references)
            IF_DEVIATION_LIMIT = 0.98
            
            if report.is_consistent and report.score >= IF_DEVIATION_LIMIT:
                logger.info(f"Visual consistency PASSED ({report.score*100}%).")
                break
            
            # Auto-Correction logic...
            # (Keeping existing logic here for brevity)
            repaired = False
            if report.feedback:
                item = report.feedback[0]
                if item.action_type == "inpaint" and item.target_area:
                    bbox = self.critic_agent.detect_mask_area(current_image, item.target_area)
                    if bbox:
                        mask_bytes = self._create_mask_from_bbox(current_image, bbox)
                        current_image = self.visual_agent.edit_image(
                            prompt=f"Surgical correction: {item.target_area}. Fix {item.description}.",
                            base_image_bytes=current_image,
                            mask_image_bytes=mask_bytes
                        )
                        repaired = True
            
            if not repaired:
                current_image = self.visual_agent.generate_image(optimized_prompt, subject_id=subject_id)
        
        final_image = current_image
            
        # --- HITL GATE 2: PRE-RENDER QA ---
        if not is_sovereign:
            approved = self._wait_for_approval(task_id, "visual_qa", {
                "score": report.score, "issues": report.issues
            }, preview_data=final_image)
            if not approved:
                raise RuntimeError("Mission rejected by human master during visual QA.")

        # 6. Production Phase
        logger.info("Starting Cinematography Phase...")
        video_data = self.director_agent.generate_video(optimized_prompt, image_bytes=final_image)
        
        production_data = {
            "title": script_data.title,
            "caption": script_data.caption,
            "video_bytes": video_data,
            "poster_image_bytes": final_image,
            "layout": layout.model_dump(),
            "look": look.model_dump()
        }

        # 7. Cost Tracking
        total_cost = self.cost_calculator.estimate_image_cost("imagen-3.0-generate-002", 1) + \
                     self.cost_calculator.estimate_video_cost("veo-3.1", 5.0)
        
        try:
            self.ledger_service.record_transaction(
                wallet_address=subject_id,
                tx_type=TransactionType.EXPENSE,
                category=TransactionCategory.API_COST,
                amount=total_cost,
                description=f"Production cost for: {script_data.title}"
            )
        except Exception as e:
            logger.error(f"Failed to record production cost: {e}")

        # 8. Staging Phase (EIC)
        logger.info("Staging for review...")
        review_path = self.eic_agent.stage_for_review(production_data, subject_id)
        
        production_data["review_path"] = review_path
        production_data["production_cost"] = total_cost
        return production_data

    async def produce_video_content_async(
        self,
        intent: str,
        mood: Mood,
        subject_id: str
    ) -> str:
        """Starts the production pipeline in the background and returns a task ID."""
        import asyncio
        import uuid
        task_id = str(uuid.uuid4())[:8]
        
        # Fire and forget the production
        asyncio.create_task(
            asyncio.to_thread(
                self.produce_video_content, 
                intent, 
                mood, 
                subject_id
            )
        )
        
        logger.info(f"Background production task {task_id} started for intent: {intent}")
        return task_id
