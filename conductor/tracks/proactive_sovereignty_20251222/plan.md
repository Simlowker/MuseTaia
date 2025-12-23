# Track Plan: Proactive Sovereignty (SMOS v2 Core Overhaul)

## Phase 1: CLI Standardization (Perception Lobe) [checkpoint: 4635415]
- [x] Task: Standardize TrendScanner to JSON Intent Objects
    - **Goal:** Migrate TrendScanner to output structured CLI-style commands instead of text summaries.
    - **Files:** `app/agents/trend_scanner.py`, `app/core/schemas/trend.py`
    - **Tech:** Pydantic, Gemini 3 Flash.
    - **Tests:** Verify trend analysis returns valid `IntentObject`.
- [x] Task: Conductor - User Manual Verification 'CLI Standardization' (Protocol in workflow.md) 4635415

## Phase 2: ADK Orchestration & A2A Protocol (Cognition Lobe) [checkpoint: 0d9a5a6]
- [x] Task: Refactor Orchestrator with Google ADK
    - **Goal:** Implement `SequentialAgent` and `ParallelAgent` for pipeline execution.
    - **Files:** `app/agents/orchestrator.py`
    - **Tech:** Google ADK.
- [x] Task: Implement A2A Context Passing (Agent-to-Agent Pipe)
    - **Goal:** Ensure secure context transfer between agents (Strategy -> EIC).
    - **Files:** `app/agents/protocols/a2a_pipe.py` (New)
    - **Tech:** Pydantic, Logger.
- [x] Task: Conductor - User Manual Verification 'ADK Orchestration' (Protocol in workflow.md) 0d9a5a6

## Phase 3: Industrial Forge (Rendering Lobe) [checkpoint: de98bd8]
- [x] Task: Integrate ComfyUI API into Production Workflow
    - **Goal:** Replace direct Imagen/Veo calls with ComfyUI nodal workflow execution.
    - **Files:** `app/core/workflow_engine.py`, `app/core/services/comfy_api.py` (New)
    - **Tech:** ComfyUI API, GKE.
- [x] Task: Finalize GKE Fast-Cloning Logic
    - **Goal:** Fully integrate the "Golden Pod" restoration in the Go Dispatcher.
    - **Files:** `infrastructure/dispatcher/worker_pool.go`
    - **Tech:** Go, GKE Snapshot API.
- [x] Task: Conductor - User Manual Verification 'Industrial Forge' (Protocol in workflow.md) de98bd8

## Phase 4: Autonomous Loop (Autonomy Lobe) [checkpoint: 71723d0]
- [x] Task: Implement Critic-led Auto-Correction
    - **Goal:** If The Critic detects >2% deviation, automatically trigger a repair (Nano Banana).
    - **Files:** `app/core/workflow_engine.py` (update).
    - **Tech:** 2% Regression Rule, Inpainting.
- [x] Task: Dynamic Wallet Allocation
    - **Goal:** Muse allocates credits based on Trend ROI estimation.
    - **Files:** `app/core/services/ledger_service.py` (update).
    - **Tech:** ROI-aware Spending logic.
- [x] Task: Conductor - User Manual Verification 'Proactive Sovereignty' (Protocol in workflow.md) 71723d0


