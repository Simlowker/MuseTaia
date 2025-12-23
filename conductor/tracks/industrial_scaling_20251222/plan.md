# Track Plan: Industrial Scaling (Pod Snapshots & CRIU)

## Phase 1: Infrastructure Readiness (CRIU & GKE)
- [x] Task: Configure Ubuntu Node Pool for CRIU 7a18b2e
    - **Goal:** Create a node pool that supports Checkpoint/Restore in Userspace (CRIU).
    - **Files:** `infrastructure/k8s/node-pool-config.yaml`
    - **Tech:** GKE, Ubuntu, CRIU.
- [x] Task: Update RuntimeClass for Checkpoint Support 7a18b2e
    - **Goal:** Ensure gVisor and the runtime class allow stateful snapshotting.
    - **Files:** `infrastructure/k8s/runtime-class.yaml` (update).
- [x] Task: Conductor - User Manual Verification 'Infra Readiness' 7a18b2e

## Phase 2: The Golden Agent (Memory Template)
- [x] Task: Implement Checkpoint Readiness Endpoint in Python 7a18b2e
    - **Goal:** Add `/internal/checkpoint-ready` to the Python agent to signal that DNA and Matrix are fully loaded.
    - **Files:** `app/main.py` (update), `app/matrix/dna_loader.py` (update).
    - **Tech:** FastAPI, Vertex AI Context Caching.
- [x] Task: Define Golden Deployment Manifest 7a18b2e
    - **Goal:** Create the deployment for the reference pod with `gke.io/pod-checkpointing` enabled.
    - **Files:** `infrastructure/k8s/snapshot-deployment.yaml`
    - **Tech:** Kubernetes, GKE Annotations.
- [x] Task: Conductor - User Manual Verification 'Golden Agent' 7a18b2e

## Phase 3: Go Dispatcher - The Restaurateur [checkpoint: a8fb98a]
- [x] Task: Implement Fast-Clone logic in Go Dispatcher
    - **Goal:** Update the dispatcher to use the GKE Checkpointing API to clone the Golden Pod instead of standard scaling.
    - **Files:** `infrastructure/dispatcher/worker_pool.go` (update).
    - **Tech:** Go, Goroutines, GKE API Simulation.
- [x] Task: Conductor - User Manual Verification 'Fast-Clone Dispatcher' (Protocol in workflow.md) a8fb98a

## Phase 4: Industrial Validation [checkpoint: 13b9e9d]
- [x] Task: Multi-Region Snapshot Persistence Test
    - **Goal:** Verify that a cloned agent retains its identity and state across node reboots.
    - **Files:** `scripts/run_visual_regression.py` (update).
    - **Tech:** GKE Snapshot Recovery.
- [x] Task: Performance Benchmarking (7x Speedup)
    - **Goal:** Measure and document the boot time difference between Cold Start and Snapshot Restore.
    - **Files:** `scripts/benchmark_boot.py`
- [x] Task: Conductor - User Manual Verification 'Industrial Validation' (Protocol in workflow.md) 13b9e9d
