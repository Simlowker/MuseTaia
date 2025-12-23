# Track Plan: Hybrid Command & HITL Integration

## Phase 1: HITL Backend Infrastructure
- [x] Task: Update StateManager for Task Persistence
    - **Goal:** Allow storing and retrieving "Pending Tasks" and "Proposals" in Redis.
    - **Files:** `app/state/db_access.py` (update), `app/core/schemas/swarm.py` (New)
    - **Tech:** Redis, Pydantic.
    - **Tests:** Verify proposal and pending task storage in Redis.
- [x] Task: Implement Proposal Endpoints
    - **Goal:** Create `/swarm/proposals` (GET) and `/swarm/approve` (POST) endpoints.
    - **Files:** `app/main.py` (update).
    - **Tests:** Verify endpoints return data from StateManager.
- [ ] Task: Conductor - User Manual Verification 'HITL Backend' (Protocol in workflow.md)

## Phase 2: Hybrid Frontend Interface [checkpoint: c3e4803]
- [x] Task: Implement Sovereign Switch (Auto/Manual)
    - **Goal:** Add the mode toggle to the cognition section.
    - **Files:** `frontend/src/app/page.tsx`, `frontend/src/context/MoodContext.tsx`, `frontend/src/services/api.ts` (update)
- [x] Task: Build Mission Proposal UI
    - **Goal:** Transform the Trends Feed into a "Suggested Commands" list with Edit/Approve/Reject actions.
    - **Files:** `frontend/src/components/TrendFeed.tsx`, `frontend/src/components/ProposalEditor.tsx` (New)
    - **Tests:** Verify modal opens with correct data when trend is clicked.
- [x] Task: Conductor - User Manual Verification 'Hybrid UI' (Protocol in workflow.md) c3e4803

## Phase 3: Validation Gates & Previews
- [x] Task: Implement Pipeline Pausing in WorkflowEngine
    - **Goal:** Update the production loop to suspend execution and wait for human signal when in "Collaborative" mode.
    - **Files:** `app/core/workflow_engine.py` (update).
    - **Tech:** Python, Redis Polling/Blocking.
    - **Tests:** Verify pipeline pauses at script and visual QA gates.
- [ ] Task: Integrate Low-Res Previews in Instant Canvas
    - **Goal:** Display intermediate render results from ComfyUI before the final 4K render.
    - **Files:** `frontend/src/app/page.tsx` (update), `app/core/services/comfy_api.py` (update).
- [ ] Task: Conductor - User Manual Verification 'Validation Gates' (Protocol in workflow.md)

## Phase 4: Full Hybrid Loop
- [ ] Task: End-to-End Collaborative Production Test
    - **Goal:** Verify: Muse Proposes -> User Edits -> Muse Renders -> Critic Check -> Success.
    - **Files:** `tests/test_hitl_workflow.py`
- [ ] Task: Conductor - User Manual Verification 'Hybrid Completion' (Protocol in workflow.md)
