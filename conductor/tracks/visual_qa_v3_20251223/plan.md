# Track Plan: The Critic & Visual QA (Governance v3)

## Phase 1: QA Schemas & Metrics
- [x] Task: Implement QAReport Schema 8ab774a
    - **Goal:** Define structured outputs for identity drift and CLIP semantic scoring.
    - **Files:** `app/core/schemas/qa.py`
- [x] Task: Finalize CriticAgent with 2% Rule 8ab774a
    - **Goal:** Implement the 0.75 similarity threshold and failure classification.
    - **Files:** `app/agents/critic_agent.py`
- [x] Task: Conductor - User Manual Verification 'QA Metrics' 8ab774a

## Phase 2: Autonomous Repair Loop
- [x] Task: Integrate Repair Loop in WorkflowEngine 8ab774a
    - **Goal:** Implement the 'REPAIR_REQUIRED' logic using inpainting (Nano Banana).
    - **Files:** `app/core/workflow_engine.py`
- [x] Task: Unit Tests for Identity Drift Rejection 8ab774a
    - **Goal:** Verify that images below the 0.75 threshold are correctly blocked.
    - **Files:** `tests/test_visual_qa.py`
- [x] Task: Conductor - User Manual Verification 'Visual Sovereignty Gate' 8ab774a
