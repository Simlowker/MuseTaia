# Track Plan: Industrial Scaling (Pod Snapshots & CRIU)

## Phase 1: Infrastructure Readiness (CRIU & GKE)
- [ ] Task: Configure Ubuntu Node Pool for CRIU
    - **Goal:** Create a node pool that supports Checkpoint/Restore in Userspace (CRIU).
    - **Files:** `infrastructure/k8s/node-pool-config.yaml`
    - **Tech:** GKE, Ubuntu, CRIU.
- [ ] Task: Update RuntimeClass for Checkpoint Support
    - **Goal:** Ensure gVisor and the runtime class allow stateful snapshotting.
    - **Files:** `infrastructure/k8s/runtime-class.yaml` (update).
- [ ] Task: Conductor - User Manual Verification 'Infra Readiness' (Protocol in workflow.md)

## Phase 2: The Golden Agent (Memory Template)
- [ ] Task: Implement Checkpoint Readiness Endpoint
    - **Goal:** Add `/internal/checkpoint-ready` to the Python agent to signal that DNA and Matrix are fully loaded.
    - **Files:** `app/main.py` (update), `app/matrix/dna_loader.py` (update).
    - **Tech:** FastAPI, Vertex AI Context Caching.
- [ ] Task: Define Golden Deployment Manifest
    - **Goal:** Create the deployment for the reference pod with `gke.io/pod-checkpointing` enabled.
    - **Files:** `infrastructure/k8s/snapshot-deployment.yaml`
- [ ] Task: Conductor - User Manual Verification 'Golden Agent' (Protocol in workflow.md)

## Phase 3: Go Dispatcher - The Restaurateur
- [ ] Task: Implement Fast-Clone logic in Go Dispatcher
    - **Goal:** Update the dispatcher to use the GKE Checkpointing API to clone the Golden Pod instead of standard scaling.
    - **Files:** `infrastructure/dispatcher/worker_pool.go` (update).
    - **Tech:** Go, Kubernetes Client-go, GKE API.
- [ ] Task: Conductor - User Manual Verification 'Fast-Clone Dispatcher' (Protocol in workflow.md)

## Phase 4: Industrial Validation
- [ ] Task: Multi-Region Snapshot Persistence Test
    - **Goal:** Verify that a cloned agent retains its identity and state across node reboots.
    - **Files:** `scripts/run_visual_regression.py` (update).
- [ ] Task: Performance Benchmarking (7x Speedup)
    - **Goal:** Measure and document the boot time difference between Cold Start and Snapshot Restore.
- [ ] Task: Conductor - User Manual Verification 'Industrial Validation' (Protocol in workflow.md)
