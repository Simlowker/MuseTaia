"""Manual verification script for Identity Persistence & Visual v2."""

import json
from app.agents.visual_virtuoso import VisualVirtuoso
from app.core.services.comfy_workflow import IdentityLockedWorkflow

def verify_visual_identity():
    print("--- 1. Testing IdentityLockedWorkflow (ComfyScript) ---")
    engine = IdentityLockedWorkflow()
    workflow = engine.build_workflow(
        prompt="Cinematic shot of the Muse in Paris.",
        face_master_path="muses/muse-01/face_master.png",
        pose_ref_path="poses/pose-sitting.png",
        pulid_weight=0.85
    )
    
    # Check key nodes
    pulid_node = workflow.get("4")
    faceid_node = workflow.get("5")
    controlnet_node = workflow.get("9")
    
    if pulid_node and faceid_node and controlnet_node:
        print("SUCCESS: Identity nodes (PuLID, FaceID, ControlNet) correctly integrated.")
        print(f"PuLID Weight: {pulid_node['inputs']['weight']}")
    else:
        print("FAILURE: Missing identity nodes in workflow.")

    print("\n--- 2. Testing VisualVirtuoso v2 Integration ---")
    virtuoso = VisualVirtuoso()
    try:
        # Conceptual call
        prompt_id = virtuoso.generate_identity_image(
            prompt="Digital jewelry close-up",
            subject_id="muse-01",
            pulid_weight=0.9
        )
        print(f"VisualVirtuoso triggered workflow. Prompt ID: {prompt_id}")
    except Exception as e:
        print(f"VisualVirtuoso call failed (simulated or real): {e}")

if __name__ == "__main__":
    verify_visual_identity()
