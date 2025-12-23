# Track Plan: Stylist & Continuity Agent

## Phase 1: Wardrobe & Prop DNA
- [x] Task: Define Wardrobe & Prop Schemas
    - **Goal:** Standardize descriptions for outfits (e.g., "Neon Mesh Jacket") and persistent props.
    - **Files:** `app/matrix/models.py` (update), `app/matrix/wardrobe_dna.py`
    - **Tech:** Pydantic.
    - **Tests:** Validate wardrobe items against the schema.
- [ ] Task: Implement Stylist Assets Manager (GCS Integration)
    - **Goal:** Manage storage and retrieval of clothing and prop reference images.
    - **Files:** `app/matrix/wardrobe_assets.py`
    - **Tech:** Google Cloud Storage.
    - **Tests:** Verify upload/retrieval of wardrobe assets.
- [ ] Task: Conductor - User Manual Verification 'Wardrobe DNA' (Protocol in workflow.md)

## Phase 2: StylistAgent - The Guardian of Look
- [ ] Task: Implement StylistAgent (Gemini 3 Pro)
    - **Goal:** Select the appropriate outfit and props for a scene based on the script, location, and Muse's mood.
    - **Files:** `app/agents/stylist_agent.py`
    - **Tech:** Gemini 3 Pro.
    - **Tests:** Verify agent selects correct outfits for different narrative contexts.
- [ ] Task: Implement Look-Reference Injection
    - **Goal:** Update the VisualAgent to use wardrobe references in the generation prompt and configuration.
    - **Files:** `app/agents/visual_agent.py` (update)
    - **Tech:** Imagen 3 (Reference images).
    - **Tests:** Verify API calls include wardrobe references.

## Phase 3: Visual Continuity QA
- [ ] Task: Update The Critic for Outfit Consistency
    - **Goal:** Teach The Critic to verify if the generated outfit and props match the selected references.
    - **Files:** `app/agents/critic_agent.py` (update)
    - **Tech:** Gemini 3 Vision.
    - **Tests:** Verify detection of "Wrong outfit" or "Missing prop".
- [ ] Task: Conductor - User Manual Verification 'Visual Continuity' (Protocol in workflow.md)

## Phase 4: Full Swarm Integration
- [ ] Task: Integrate Stylist into WorkflowEngine
    - **Goal:** Orchestrate Narrative -> Stylist -> Architect -> Visual -> Critic to ensure complete identity, look, and environment consistency.
    - **Files:** `app/core/workflow_engine.py` (update)
    - **Tech:** Python.
    - **Tests:** End-to-end integration test with specific outfit and location.
- [ ] Task: Conductor - User Manual Verification 'Full Swarm Integration' (Protocol in workflow.md)
