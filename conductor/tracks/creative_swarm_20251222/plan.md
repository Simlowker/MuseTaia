# Track Plan: Build the Creative Swarm (Narrative, Visual, & Director)

## Phase 1: Narrative Engine (The Screenwriter) [checkpoint: 54e5af8]
- [x] Task: Implement Narrative Agent (Gemini 3 Pro)
    - **Goal:** Create the agent responsible for writing scripts, captions, and story arcs consistent with the Muse's persona.
    - **Files:** `app/agents/narrative_agent.py`, `app/agents/prompts/narrative.py`
    - **Tech:** Gemini 3 Pro, Vertex AI Context Caching.
    - **Tests:** Verify script generation adheres to persona constraints (tone, forbidden topics).
- [x] Task: Define Screenplay JSON Schema
    - **Goal:** Standardize the output format for downstream agents (Visual/Director).
    - **Files:** `app/core/schemas/screenplay.py`
    - **Tech:** Pydantic.
    - **Tests:** Validate sample scripts against the schema.
- [x] Task: Conductor - User Manual Verification 'Narrative Engine' (Protocol in workflow.md) 54e5af8

## Phase 2: Visual Virtuoso (The Photographer)
- [x] Task: Implement Visual Agent (Imagen 3)
    - **Goal:** Generate high-fidelity keyframes using Subject Guidance to maintain identity.
    - **Files:** `app/agents/visual_agent.py`
    - **Tech:** Imagen 3 API (via Vertex AI), Signature Assets Manager.
    - **Tests:** Verify image generation requests include correct reference assets.
- [x] Task: Implement Prompt Engineering Layer
    - **Goal:** Automatically convert high-level screenplay scene descriptions into optimized technical prompts for Imagen.
    - **Files:** `app/core/utils/prompt_optimizer.py`
    - **Tech:** Gemini 3 Flash (for rewriting).
    - **Tests:** Test conversion of "She walks on the beach" to "Cinematic wide shot, golden hour...".
- [ ] Task: Conductor - User Manual Verification 'Visual Virtuoso' (Protocol in workflow.md)

## Phase 3: The Cinematographer (The Director)
- [ ] Task: Implement Director Agent (Veo 3.1)
    - **Goal:** Generate consistent video clips from keyframes and motion descriptions.
    - **Files:** `app/agents/director_agent.py`
    - **Tech:** Veo 3.1 API, Image-to-Video.
    - **Tests:** Verify API calls for video generation (mocked for cost).
- [ ] Task: Integration Test: Text -> Image -> Video Pipeline
    - **Goal:** Verify the full production chain from a text concept to a final video asset.
    - **Files:** `tests/test_production_pipeline.py`
    - **Tech:** Pytest, Integration testing.
    - **Tests:** End-to-end flow execution.
- [ ] Task: Conductor - User Manual Verification 'The Cinematographer' (Protocol in workflow.md)

## Phase 4: Swarm Orchestration & Review
- [ ] Task: Integrate "The Critic" into the Production Loop
    - **Goal:** Automate the rejection and regeneration of assets that fail visual consistency checks.
    - **Files:** `app/agents/orchestrator.py` (update), `app/core/workflow_engine.py`
    - **Tech:** Python, CriticAgent.
    - **Tests:** Simulate bad assets and verify the loop triggers regeneration.
- [ ] Task: Implement EIC (Editor-in-Chief) Routing
    - **Goal:** Route approved assets to a "Ready for Review" state/folder for the user.
    - **Files:** `app/agents/eic_agent.py`
    - **Tech:** Google Cloud Storage, Task Routing.
    - **Tests:** Verify final assets are correctly staged.
- [ ] Task: Conductor - User Manual Verification 'Swarm Orchestration' (Protocol in workflow.md)
