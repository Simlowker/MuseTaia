# Track Plan: High Compute Burst & Skill Sandboxing (Scale v1)

## Phase 1: Massive Parallelism (Best-of-N)
- [x] Task: Implement 'Burst' Logic in Go Dispatcher 7a18b2e
    - **Goal:** Allow the dispatcher to clone N pods simultaneously for a single high-priority intent (VVS > 90).
    - **Files:** `infrastructure/dispatcher/worker_pool.go`, `infrastructure/dispatcher/server.go`
- [x] Task: Update Orchestrator for Consensus Selection 7a18b2e
    - **Goal:** Modify the Runner to wait for N samples and use `The Critic` as an arbitrator.
    - **Files:** `app/agents/orchestrator.py`

## Phase 2: Skill Sandboxing (E2B-Style)
- [x] Task: Implement Agent Scratchpad (Sandbox) 7a18b2e
    - **Goal:** Create a temporary, isolated GCS/Redis directory for each task where agents can 'draft' without polluting the Matrix.
    - **Files:** `app/state/db_access.py`, `app/agents/protocols/a2a_pipe.py`
- [x] Task: Define 'Skill' Registry 7a18b2e
    - **Goal:** Standardize a set of executable Python 'skills' that agents can run in their sandbox (ex: complex data math, image meta-analysis).
    - **Files:** `app/agents/tools/skills_registry.py`

## Phase 3: Validation & Benchmark
- [x] Task: End-to-End Burst Test 7a18b2e
    - **Goal:** Trigger a VVS 95 trend and verify that 10 pods are cloned and one 'Best' result is delivered in < 15s.
    - **Files:** `scripts/burst_consensus_test.py`
