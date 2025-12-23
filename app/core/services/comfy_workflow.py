"""Identity-Locked Workflow implementation using ComfyScript concepts."""

from typing import Dict, Any, List, Optional

class IdentityLockedWorkflow:
    """Generates ComfyUI workflow JSON for identity-locked production.
    
    Integrates:
    - PuLID (Primary Anchor)
    - IP-Adapter FaceID (Reinforcement)
    - ControlNet (Pose Control)
    """

    def __init__(self, checkpoint: str = "sdxl_base_v1.0.safetensors"):
        self.checkpoint = checkpoint

    def build_workflow(
        self, 
        prompt: str, 
        face_master_path: str,
        pose_ref_path: Optional[str] = None,
        pulid_weight: float = 0.8,
        faceid_weight: float = 0.5,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Builds the nodal graph for ComfyUI API with dynamic parameters."""
        
        # Inject dynamic look and lighting into prompt
        enhanced_prompt = prompt
        if parameters:
            look = parameters.get("look", "")
            lighting = parameters.get("lighting", "")
            if look: enhanced_prompt += f", {look} style"
            if lighting: enhanced_prompt += f", {lighting} lighting"

        # This is a conceptual mapping of the Python-based ComfyScript 
        workflow = {
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": self.checkpoint}},
            "2": {"class_type": "CLIPTextEncode", "inputs": {"text": enhanced_prompt, "clip": ["1", 1]}},

            "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "low quality, blurry, distorted", "clip": ["1", 1]}},
            
            # Identity Anchoring (PuLID)
            "4": {
                "class_type": "PuLID_Apply",
                "inputs": {
                    "model": ["1", 0],
                    "image": face_master_path,
                    "method": "insightface",
                    "weight": pulid_weight,
                    "gn_weight": 1.0
                }
            },
            
            # FaceID Reinforcement
            "5": {
                "class_type": "IPAdapterFaceID",
                "inputs": {
                    "model": ["4", 0],
                    "image": face_master_path,
                    "weight": faceid_weight,
                    "noise": 0.0
                }
            },
            
            # KSampler (Final Rendering)
            "6": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": 42,
                    "steps": 30,
                    "cfg": 7.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["5", 0],
                    "positive": ["2", 0],
                    "negative": ["3", 0],
                    "latent_image": ["7", 0]
                }
            },
            
            # Empty Latent (Dimension)
            "7": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
            
            # VAE Decode
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},

            # Depth Analysis (Depth Anything V2)
            "10": {
                "class_type": "DepthAnythingV2_Estimator",
                "inputs": {
                    "image": ["8", 0],
                    "model": "depth_anything_v2_vitl.safetensors"
                }
            },

            # Bokeh / Cinematic Blur
            "11": {
                "class_type": "LensBokeh",
                "inputs": {
                    "image": ["8", 0],
                    "depth_map": ["10", 0],
                    "focus_distance": 0.5,
                    "aperture": 2.8,
                    "blur_radius": 15.0
                }
            }
        }


        if pose_ref_path:
            workflow["9"] = {
                "class_type": "ControlNetApply",
                "inputs": {
                    "model": ["5", 0],
                    "control_net": "control_openpose.safetensors",
                    "image": pose_ref_path,
                    "strength": 0.7
                }
            }
            # Re-wire KSampler to use ControlNet model
            workflow["6"]["inputs"]["model"] = ["9", 0]

        return workflow
