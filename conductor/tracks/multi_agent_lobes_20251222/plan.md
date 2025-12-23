# Track Plan: Functional Lobe Architecture (SMOS Swarm v2)

## Phase 1: Perception Lobe (The Scout Lobe)
- [x] Task: Implement The TrendScout Tools 25771ce
    - **Goal:** Integrate social scraping and niche filtering.
    - **Files:** `app/agents/trend_scout.py`, `app/core/services/scraper.py`
    - **Tech:** Gemma 2 27B, Apify (Conceptual).
- [ ] Task: Implement The Librarian (RAG Specialist)
    - **Goal:** Enable viral structure extraction and semantic retrieval.
    - **Files:** `app/agents/librarian.py`
    - **Tech:** Vertex AI Vector Search.
- [ ] Task: Conductor - User Manual Verification 'Perception Lobe' (Protocol in workflow.md)

## Phase 2: High Cognition Lobe (The Brain)
- [ ] Task: Refactor RootAgent for ADK Workflow Management
    - **Goal:** Standardize intent parsing and validation gate logic.
    - **Files:** `app/agents/root_agent.py` (update).
    - **Tech:** Google ADK.
- [ ] Task: Refactor The Strategist
    - **Goal:** Guardian of long-term narrative and budget allocation logic.
    - **Files:** `app/agents/strategist.py`
    - **Tech:** Gemini 3 Pro, Context Cache.
- [ ] Task: Conductor - User Manual Verification 'Brain Lobe' (Protocol in workflow.md)

## Phase 3: Creative Studio Lobe (Production)
- [ ] Task: Implement Narrative Architect & Visual Virtuoso Integration
    - **Goal:** Refine script-to-image pipeline with ComfyUI Nodal API.
    - **Files:** `app/agents/narrative_architect.py`, `app/agents/visual_virtuoso.py`
    - **Tech:** Imagen 3, ComfyUI.
- [ ] Task: Implement Motion Engineer (Veo 3.1)
    - **Goal:** Complete the lip-sync and cinematic animation hand-off.
    - **Files:** `app/agents/motion_engineer.py`
    - **Tech:** Veo 3.1.
- [ ] Task: Conductor - User Manual Verification 'Creative Studio' (Protocol in workflow.md)

## Phase 4: Governance Lobe (Forge Control)
- [ ] Task: Finalize The Critic & Financial Accountant
    - **Goal:** Ensure 2% deviation rule enforcement and real-time ledger settlement.
    - **Files:** `app/agents/critic_agent.py`, `app/agents/finance_agent.py`
- [ ] Task: End-to-End CLI System Test
    - **Goal:** Run `smos produce --intent ...` and verify full lobe orchestration.
- [ ] Task: Conductor - User Manual Verification 'System Completion' (Protocol in workflow.md)
