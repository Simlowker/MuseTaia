# Track Plan: The World Engine (ArchitectAgent)

## Phase 1: Environmental Anchors & Registry
- [ ] Task: Define Environmental DNA Schema (Locations & Objects)
    - **Goal:** Standardize how locations (e.g., "Paris Studio") and recurring objects (e.g., "Blue Velvet Sofa") are defined.
    - **Files:** `app/matrix/models.py` (update), `app/matrix/world_dna.py`
    - **Tech:** Pydantic.
    - **Tests:** Validate environmental objects against the schema.
- [ ] Task: Implement World Assets Manager (GCS Integration)
    - **Goal:** Manage the storage and retrieval of environmental reference images (Backgrounds, Objects).
    - **Files:** `app/matrix/world_assets.py`
    - **Tech:** Google Cloud Storage.
    - **Tests:** Verify upload/retrieval of "Location" assets.
- [ ] Task: Conductor - User Manual Verification 'Environmental Anchors' (Protocol in workflow.md)

## Phase 2: ArchitectAgent - The Space Guardian
- [ ] Task: Implement ArchitectAgent (Gemini 3 Pro)
    - **Goal:** Create the agent responsible for selecting and maintaining the scene's environment based on the narrative.
    - **Files:** `app/agents/architect_agent.py`
    - **Tech:** Gemini 3 Pro, Context Caching.
    - **Tests:** Verify agent selects correct recurring locations for a given script.
- [ ] Task: Implement Environment Reference Injection
    - **Goal:** Update the VisualAgent to accept and use environmental reference images in addition to subject references.
    - **Files:** `app/agents/visual_agent.py` (update)
    - **Tech:** Imagen 3 (Reference images).
    - **Tests:** Verify API calls include both Subject and Environment references.

## Phase 3: Spatial QA & Continuity
- [ ] Task: Update The Critic for Environmental Consistency
    - **Goal:** Teach The Critic to detect drift in backgrounds and recurring props.
    - **Files:** `app/agents/critic_agent.py` (update), `app/core/schemas/qa.py` (update)
    - **Tech:** Gemini 3 Vision.
    - **Tests:** Verify detection of "Wrong furniture" or "Background mismatch".
- [ ] Task: Conductor - User Manual Verification 'Spatial QA & Continuity' (Protocol in workflow.md)

## Phase 4: Full Reality Persistence
- [ ] Task: Integrate World Engine into WorkflowEngine
    - **Goal:** Orchestrate the Narrative -> Architect -> Visual -> Critic loop to ensure Muse + Environment consistency.
    - **Files:** `app/core/workflow_engine.py` (update)
    - **Tech:** Python.
    - **Tests:** End-to-end integration test with persistent location.
- [ ] Task: Conductor - User Manual Verification 'Full Reality Persistence' (Protocol in workflow.md)
