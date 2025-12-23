# Track Plan: Identity Persistence & ComfyScript (Visual v2)

## Phase 1: Nodal Architecture & Identity Lock
- [x] Task: Implement Identity-Locked Workflow (ComfyScript) aa665cc
    - **Goal:** Create the Python-based workflow integrating PuLID and IP-Adapter FaceID.
    - **Files:** `app/core/services/comfy_workflow.py`
- [x] Task: Integrate Signature Assets (Face Master) aa665cc
    - **Goal:** Ensure the 'Genesis Face' is correctly injected into every generation.
    - **Files:** `app/agents/visual_virtuoso.py`
- [x] Task: Conductor - User Manual Verification 'Identity Workflow' aa665cc

## Phase 2: Visual Virtuoso Upgrade
- [x] Task: Refactor VisualVirtuoso for Dynamic Workflows aa665cc
    - **Goal:** Allow the agent to adjust PuLID weights and ControlNet poses via code.
    - **Files:** `app/agents/visual_virtuoso.py`
- [x] Task: Implement Identity Consistency Unit Tests aa665cc
    - **Goal:** Use cosine similarity (InsightFace logic) to verify identity persistence.
    - **Files:** `tests/test_visual_identity.py`
- [x] Task: Conductor - User Manual Verification 'Visual Sovereignty' aa665cc
