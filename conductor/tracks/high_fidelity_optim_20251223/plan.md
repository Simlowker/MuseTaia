# Track Plan: High-Fidelity Optimization & Production Value (Quality v1)

## Phase 1: Cognitive Consolidation (Memory & Strategy)
- [x] Task: Upgrade Matrix Context Caching 7a18b2e
    - **Goal:** Implement explicit caching for Style Bibles and few-shot examples via google-genai SDK.
    - **Files:** `app/matrix/context_cache.py`, `app/matrix/dna_loader.py`
- [x] Task: Implement Dynamic Compute Allocation (BoN) 7a18b2e
    - **Goal:** Link VVS score to N-sampling depth (VVS > 80 -> N=5).
    - **Files:** `app/agents/finance_agent.py`

## Phase 2: Narrative Excellence (Attention Dynamics)
- [x] Task: Refactor ScriptOutput Schema ac8fe24
    - **Goal:** Add `attention_dynamics` and temporal markers for Pattern Interruption.
    - **Files:** `app/agents/narrative_agent.py`, `app/core/schemas/screenplay.py`
- [x] Task: Implement Pattern Interruption Logic ac8fe24
    - **Goal:** Force visual/audio shifts every 8 seconds to maintain retention.
    - **Files:** `app/agents/narrative_architect.py`

## Phase 3: The Forge Mastery (Visual & Temporal)
- [x] Task: Integrate Depth Anything V2 8ab774a
    - **Goal:** Add physical depth and bokeh to ComfyUI nodal templates.
    - **Files:** `app/core/services/comfy_workflow.py`
- [x] Task: Implement Temporal Prompting for Veo 3.1 8ab774a
    - **Goal:** Add syntax `[00:00-00:02]` to drive precise motion sequences.
    - **Files:** `app/agents/director_agent.py`

## Phase 4: Industrial Quality Loop (VideoScore2)
- [x] Task: Implement VideoScore Service 8ab774a
    - **Goal:** Integrate VideoScore2 model for automated Best-of-N arbitration.
    - **Files:** `app/core/services/video_score_service.py`
- [x] Task: Extend CriticAgent for Physical Artifacts 8ab774a
    - **Goal:** Use Bounding Boxes to detect hands/shadows anomalies via Gemini Vision.
    - **Files:** `app/agents/critic_agent.py`
