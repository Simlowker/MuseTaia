"""Visual Virtuoso for high-fidelity nodal production integration (v2)."""

from typing import List, Optional, Dict, Any
from app.agents.visual_agent import VisualAgent
from app.core.services.comfy_api import ComfyUIClient
from app.core.services.comfy_workflow import IdentityLockedWorkflow

class VisualVirtuoso(VisualAgent):
    """Agent that executes high-fidelity visual production via Nodal APIs.
    
    This agent represents the 'Creative Studio Lobe'.
    v2: Uses IdentityLockedWorkflow (PuLID + FaceID) for absolute consistency.
    """

    def __init__(self, model_name: str = "imagen-3.0-generate-002", comfy_address: str = "localhost:8188"):
        super().__init__(model_name)
        self.comfy_client = ComfyUIClient(server_address=comfy_address)
        self.workflow_engine = IdentityLockedWorkflow()

    def generate_identity_image(
        self, 
        prompt: str, 
        subject_id: str,
        pose_ref_path: Optional[str] = None,
        pulid_weight: float = 0.8
    ) -> str:
        """Triggers a high-fidelity image generation with locked identity.
        
        Args:
            prompt: The production prompt.
            subject_id: The Muse identity to lock.
            pose_ref_path: Optional pose reference image.
            pulid_weight: How strong to apply PuLID (0.0 to 1.0).
            
        Returns:
            str: The ComfyUI prompt ID.
        """
        # 1. Resolve Signature Assets (Face Master)
        face_master_path = f"muses/{subject_id}/face_master.png"
        
        # 2. Build the dynamic workflow
        workflow = self.workflow_engine.build_workflow(
            prompt=prompt,
            face_master_path=face_master_path,
            pose_ref_path=pose_ref_path,
            pulid_weight=pulid_weight
        )
        
        # 3. Queue via API
        prompt_id = self.comfy_client.queue_prompt(workflow)
        return prompt_id

    def retrieve_nodal_output(self, prompt_id: str) -> Optional[bytes]:
        """Retrieves the final output of a nodal workflow."""
        return self.comfy_client.get_output_data(prompt_id)