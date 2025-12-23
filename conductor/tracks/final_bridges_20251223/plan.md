# Track Plan: Final Bridges & Autonomous Transmission (Integration v2)

## Phase 1: The ADK Runner (The Transmission)
- [x] Task: Implement TaskGraph Executor 7a18b2e
    - **Goal:** Create a 'Runner' that traverses the TaskGraph and dispatches instructions to specialized agents via A2A.
    - **Files:** `app/agents/orchestrator.py`
- [x] Task: Implement A2A Context Pipe 7a18b2e
    - **Goal:** Ensure data (prompts, asset paths) flows correctly between sequential and parallel nodes.
    - **Files:** `app/agents/protocols/a2a_pipe.py`

## Phase 2: Industrial ComfyUI Bridge
- [x] Task: Implement Dynamic Node Mapping 7a18b2e
    - **Goal:** Map CLI-style intent parameters directly into ComfyUI JSON nodes.
    - **Files:** `app/core/services/comfy_workflow.py`
- [x] Task: Implement Async Output Polling 7a18b2e
    - **Goal:** Replace placeholder retrieval with a robust async queue watcher for GKE pods.
    - **Files:** `app/core/services/comfy_api.py`

## Phase 3: Autonomous Loop & Financial Safety
- [x] Task: Implement Trend-to-Production Daemon 7a18b2e
    - **Goal:** Background task that triggers production when VVS > 50.0.
    - **Files:** `app/main.py`
- [x] Task: Implement Financial Rollback (Refunds) 7a18b2e
    - **Goal:** Add logic to recredit the Sovereign Wallet if a GKE production task fails.
    - **Files:** `app/agents/finance_agent.py`, `app/core/services/ledger_service.py`
