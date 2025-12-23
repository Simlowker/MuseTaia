# Track Plan: Operational Launch Readiness

## Phase 1: Environment & Secrets Configuration
- [x] Task: Finalize Environment Variables
    - **Goal:** Ensure `.env` and `frontend/.env.local` are correctly structured for production/dev.
    - **Files:** `.env.example`, `frontend/.env.local.example`
- [x] Task: Implement Bootstrap Script
    - **Goal:** Create a script to initialize the first MoodState and verify GCP API access.
    - **Files:** `scripts/bootstrap_system.py`
    - **Tests:** Verify script initializes Redis keys correctly.
- [ ] Task: Conductor - User Manual Verification 'Configuration' (Protocol in workflow.md)

## Phase 2: Real-time Frontend Synchronization
- [x] Task: Implement Mood Polling in Context
    - **Goal:** Update `MoodContext.tsx` to fetch real-time state from the backend.
    - **Files:** `frontend/src/context/MoodContext.tsx`
    - **Tech:** React `useEffect`, polling.
- [x] Task: Wire Swarm Control Buttons
    - **Goal:** Connect the "Discuss" and "Trigger" buttons to the `smosApi.triggerProduction` call.
    - **Files:** `frontend/src/app/page.tsx` (update).
    - **Tests:** Verify production request is sent to backend.
- [ ] Task: Conductor - User Manual Verification 'Frontend Sync' (Protocol in workflow.md)

## Phase 3: Financial & QA Data Flow
- [x] Task: Connect Ledger Dashboard to Real Data
    - **Goal:** Replace mock ledger data with actual transaction history from `LedgerService`.
    - **Files:** `frontend/src/app/ledger/page.tsx` (update).
    - **Tests:** Verify ledger table displays real backend records.
- [x] Task: Wire Critic Feedback to DriftVisualizer
    - **Goal:** Ensure the Drift Visualizer displays real consistency scores from the production loop.
    - **Files:** `frontend/src/app/forge/page.tsx` (update).
    - **Tests:** Verify visualizer reacts to score changes (Pass/Fail colors).
- [x] Task: Conductor - User Manual Verification 'Data Flow' (Protocol in workflow.md) [checkpoint: PENDING]

## Phase 4: Final Documentation & Launch
- [x] Task: Create Launch Guide (README Update)
    - **Goal:** Provide clear instructions for launching the full stack (Infrastructure, Backend, Frontend).
    - **Files:** `README.md`
- [x] Task: Final End-to-End System Smoke Test
    - **Goal:** Verify that a user interaction leads to a real GCS asset generation and a ledger update.
- [x] Task: Conductor - User Manual Verification 'Launch Readiness' (Protocol in workflow.md) [checkpoint: PENDING]
