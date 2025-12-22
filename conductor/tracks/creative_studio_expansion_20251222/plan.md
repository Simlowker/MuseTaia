# Track Plan: Creative Studio Expansion (Actions & Tools)

## Phase 1: Visual Studio Tools (Imagen 3)
- [x] Task: Implement Inpainting & Editing Capabilities
    - **Goal:** Enable the VisualAgent to repair specific areas of an image using masks.
    - **Files:** `app/agents/visual_agent.py`
    - **Tech:** Imagen 3 Editing API (Mask-based editing).
    - **Tests:** Verify edit requests with mock masks.
- [x] Task: Implement Style & Subject Reference Configuration
    - **Goal:** Allow injection of "Signature Assets" as style/subject references to ensure aesthetic consistency.
    - **Files:** `app/agents/visual_agent.py`
    - **Tech:** Imagen 3 `style_reference` and `subject_reference` parameters.
    - **Tests:** Verify API calls include reference image config.

## Phase 2: Director's Chair (Veo 3.1)
- [x] Task: Implement Cinematic Camera Controls
    - **Goal:** Map the `Screenplay` schema's camera movements to Veo 3.1 prompt structures.
    - **Files:** `app/agents/director_agent.py`
    - **Tech:** Prompt engineering for camera control (Pan, Tilt, Zoom).
    - **Tests:** Verify prompt construction includes camera directives.
- [x] Task: Implement Ingredients-to-Video (Persistence)
    - **Goal:** Pass multiple reference images (Subject + Style) to Veo to ensure character persistence.
    - **Files:** `app/agents/director_agent.py`
    - **Tech:** Veo 3.1 Multi-image input.
    - **Tests:** Verify API calls with multiple image references.

## Phase 3: The Critic's Eye (Surgical QA)
- [x] Task: Implement Drift Vector Feedback
    - **Goal:** Update The Critic to return specific actionable feedback (e.g., "Lighting too dark") instead of just boolean.
    - **Files:** `app/agents/critic_agent.py`, `app/core/schemas/qa.py`
    - **Tech:** Gemini 3 Vision, Structured Output.
    - **Tests:** Verify generation of detailed feedback objects.
- [x] Task: Implement Automatic Mask Generation (Conceptual)
    - **Goal:** Allow The Critic to identify coordinates/areas for repair (e.g., "Face area").
    - **Files:** `app/agents/critic_agent.py`
    - **Tech:** Gemini 3 Vision (Bounding Box detection).
    - **Tests:** Verify return of bounding box coordinates for specific features.

## Phase 4: Advanced Orchestration (Feedback Loop) [checkpoint: de98bd8]
- [x] Task: Implement Iterative Repair Loop
    - **Goal:** Update WorkflowEngine to use Critic's feedback to trigger specific "Repair" actions (Inpainting) instead of full regeneration.
    - **Files:** `app/core/workflow_engine.py`
    - **Tech:** Python, State Machine logic.
    - **Tests:** Simulate a flow: Generate -> Critic Reject (Face) -> Inpaint Face -> Critic Accept.
- [x] Task: Conductor - User Manual Verification 'Creative Studio Expansion' (Protocol in workflow.md) de98bd8
