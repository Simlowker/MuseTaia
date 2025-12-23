# Track Plan: Functional Lobe Architecture (SMOS Swarm v2)

## Phase 1: Perception Lobe (The Scout Lobe) [checkpoint: 89da3ac]
- [x] Task: Implement The TrendScout Tools 25771ce
    - **Goal:** Integrate social scraping and niche filtering.
    - **Files:** `app/agents/trend_scout.py`, `app/core/services/scraper.py`
    - **Tech:** Gemma 2 27B, Apify (Conceptual).
- [x] Task: Implement The Librarian (RAG Specialist) 666721f
    - **Goal:** Enable viral structure extraction and semantic retrieval.
    - **Files:** `app/agents/librarian.py`
    - **Tech:** Vertex AI Vector Search.
- [x] Task: Conductor - User Manual Verification 'Perception Lobe' (Protocol in workflow.md) 89da3ac

## Phase 2: High Cognition Lobe (The Brain) [checkpoint: db582eb]
- [x] Task: Refactor RootAgent for ADK Workflow Management a3058a1
    - **Goal:** Standardize intent parsing and validation gate logic.
    - **Files:** `app/agents/root_agent.py` (update).
    - **Tech:** Google ADK.
- [x] Task: Refactor The Strategist a3058a1
    - **Goal:** Guardian of long-term narrative and budget allocation logic.
    - **Files:** `app/agents/strategist.py`
    - **Tech:** Gemini 3 Pro, Context Cache.
- [x] Task: Conductor - User Manual Verification 'Brain Lobe' (Protocol in workflow.md) db582eb

## Phase 3: Creative Studio Lobe (Production) [checkpoint: 56c367b]
- [x] Task: Implement Narrative Architect & Visual Virtuoso Integration 2f6d5d0
    - **Goal:** Refine script-to-image pipeline with ComfyUI Nodal API.
    - **Files:** `app/agents/narrative_architect.py`, `app/agents/visual_virtuoso.py`
    - **Tech:** Imagen 3, ComfyUI.
- [x] Task: Implement Motion Engineer (Veo 3.1) 2f6d5d0
    - **Goal:** Complete the lip-sync and cinematic animation hand-off.
    - **Files:** `app/agents/motion_engineer.py`
    - **Tech:** Veo 3.1.
- [x] Task: Conductor - User Manual Verification 'Creative Studio' (Protocol in workflow.md) 56c367b

## Phase 4: Governance Lobe (Forge Control)
- [x] Task: Finalize The Critic & Financial Accountant f277563
    - **Goal:** Ensure 2% deviation rule enforcement and real-time ledger settlement.
    - **Files:** `app/agents/critic_agent.py`, `app/agents/finance_agent.py`
- [x] Task: End-to-End CLI System Test f277563
    - **Goal:** Run `smos produce --intent ...` and verify full lobe orchestration.
- [ ] Task: Conductor - User Manual Verification 'System Completion' (Protocol in workflow.md)
