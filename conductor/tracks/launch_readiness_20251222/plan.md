# Track Plan: Operational Launch Readiness

## Phase 1: Environment & Secrets Configuration
- [ ] Task: Finalize Environment Variables
    - **Goal:** Ensure `.env` and `frontend/.env.local` are correctly structured for production/dev.
    - **Files:** `.env.example`, `frontend/.env.local.example`
- [ ] Task: Implement Bootstrap Script
    - **Goal:** Create a script to initialize the first MoodState and verify GCP API access.
    - **Files:** `scripts/bootstrap_system.py`
- [ ] Task: Conductor - User Manual Verification 'Configuration' (Protocol in workflow.md)

## Phase 2: Real-time Frontend Synchronization
- [ ] Task: Implement Mood Polling in Context
    - **Goal:** Update `MoodContext.tsx` to fetch real-time state from the backend.
    - **Files:** `frontend/src/context/MoodContext.tsx`
    - **Tech:** React `useEffect`, polling.
- [ ] Task: Wire Swarm Control Buttons
    - **Goal:** Connect the "Discuss" and "Trigger" buttons to the `smosApi.triggerProduction` call.
    - **Files:** `frontend/src/app/page.tsx` (update).
- [ ] Task: Conductor - User Manual Verification 'Frontend Sync' (Protocol in workflow.md)

## Phase 3: Financial & QA Data Flow
- [ ] Task: Connect Ledger Dashboard to Real Data
    - **Goal:** Replace mock ledger data with actual transaction history from `LedgerService`.
    - **Files:** `frontend/src/app/ledger/page.tsx` (update).
- [ ] Task: Wire Critic Feedback to DriftVisualizer
    - **Goal:** Ensure the Drift Visualizer displays real consistency scores from the production loop.
    - **Files:** `frontend/src/app/forge/page.tsx` (update).
- [ ] Task: Conductor - User Manual Verification 'Data Flow' (Protocol in workflow.md)

## Phase 4: Final Documentation & Launch
- [ ] Task: Create Launch Guide (README Update)
    - **Goal:** Provide clear instructions for launching the full stack (Infrastructure, Backend, Frontend).
    - **Files:** `README.md`
- [ ] Task: Final End-to-End System Smoke Test
    - **Goal:** Verify that a user interaction leads to a real GCS asset generation and a ledger update.
- [ ] Task: Conductor - User Manual Verification 'Launch Readiness' (Protocol in workflow.md)
