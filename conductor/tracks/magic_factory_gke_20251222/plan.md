# Track Plan: Magic Factory GKE (Industrial Deployment & Scaling)

## Phase 1: Containerization of the Swarm
- [ ] Task: Create Optimized Dockerfile for Python Agents
    - **Goal:** Package the entire Python app (Agents, Core, State) into a deployable container.
    - **Files:** `Dockerfile`, `.dockerignore`
    - **Tech:** Docker, Multi-stage builds.
    - **Tests:** Build image and run basic "ping" test inside container.
- [ ] Task: Define Local Orchestration with Docker Compose
    - **Goal:** Verify the stack (App + Redis) works in containers.
    - **Files:** `docker-compose.yml`
    - **Tech:** Docker Compose.
    - **Tests:** `docker-compose up` results in functional agents.
- [ ] Task: Conductor - User Manual Verification 'Containerization' (Protocol in workflow.md)

## Phase 2: Kubernetes Manifests (The Factory Floor)
- [ ] Task: Define GKE Deployment Manifests
    - **Goal:** Create K8s configurations for deploying the Swarm.
    - **Files:** `infrastructure/k8s/deployment.yaml`, `infrastructure/k8s/service.yaml`
    - **Tech:** Kubernetes, YAML.
    - **Settings:** Replicas=3, Resources limits.
- [ ] Task: Configure gVisor Sandbox
    - **Goal:** Enable secure isolation for the agents using gVisor (RuntimeClass).
    - **Files:** `infrastructure/k8s/runtime-class.yaml` (or update deployment).
    - **Tech:** gVisor (gvisor.io).
- [ ] Task: Conductor - User Manual Verification 'Kubernetes Manifests' (Protocol in workflow.md)

## Phase 3: High-Performance Go Dispatcher
- [ ] Task: Initialize Go Module for Dispatcher
    - **Goal:** Set up the Go project structure for the high-concurrency scheduler.
    - **Files:** `infrastructure/dispatcher/go.mod`, `infrastructure/dispatcher/main.go`
    - **Tech:** Go (Golang).
- [ ] Task: Implement gRPC/HTTP Interface for Job Dispatching
    - **Goal:** Create a Go service that receives high-volume trigger requests and dispatches them to the Python Swarm pods.
    - **Files:** `infrastructure/dispatcher/server.go`, `infrastructure/dispatcher/worker_pool.go`
    - **Tech:** Goroutines, Channels.
    - **Tests:** Go unit tests for worker pool logic.
- [ ] Task: Conductor - User Manual Verification 'Go Dispatcher' (Protocol in workflow.md)

## Phase 4: CI/CD & Optimization
- [ ] Task: Define Cloud Build Configuration
    - **Goal:** Automate the build and deploy process.
    - **Files:** `cloudbuild.yaml`
    - **Tech:** Google Cloud Build.
- [ ] Task: Conductor - User Manual Verification 'CI/CD & Optimization' (Protocol in workflow.md)
