# Track Plan: High-Level Autonomy & Multimodal Voice (Final v1)

## Phase 1: HLP/Worker Dichotomy (Architecture Refinement)
- [x] Task: Modularize Agents into 'Workers' 543a2f3
    - **Goal:** Transform Narrative, Visual, and Audio agents into pluggable modules.
    - **Files:** `app/agents/base_worker.py`, `app/agents/registry.py`
- [x] Task: Refactor Strategist into High-Level Planner (HLP) f09161c
    - **Goal:** Decouple strategy from execution. HLP only handles intents and budgets.
    - **Files:** `app/agents/strategist.py`

## Phase 2: Sovereign Voice (Audio Lobe)
- [x] Task: Implement Sovereign TTS Service 8ab774a
    - **Goal:** High-fidelity voice cloning integration.
    - **Files:** `app/core/services/audio_service.py`
- [x] Task: Integrate Audio-to-LipSync 8ab774a
    - **Goal:** Drive facial motion from generated audio.
    - **Files:** `app/agents/motion_engineer.py`
- [x] Task: Vocal QA (The Critic Expansion) 8ab774a
    - **Goal:** Verify vocal consistency against the Muse's DNA.
    - **Files:** `app/agents/critic_agent.py`
