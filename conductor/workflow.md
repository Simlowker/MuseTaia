# SMOS v2 - Operational Workflows & Protocols

**Status:** Golden Build (Production Ready)
**Date:** December 23, 2025

---

## 1. Development Workflow

### A. The "Track" System
We use a **Conductor-driven** development process. Each major feature or fix is encapsulated in a "Track":
1.  **Plan:** Create a `plan.md` in `conductor/tracks/<track_name>/`.
2.  **Execute:** Implement changes atomically.
3.  **Verify:** Run relevant unit tests (`pytest`).
4.  **Close:** Mark the track as `[x]` in `conductor/tracks.md`.

### B. Testing Protocol
*   **Unit Tests (Pre-Commit):** Must pass 100%. Run `pytest tests -m "not integration"`.
    *   *Scope:* Logic, Schemas, Mocks.
*   **Integration Tests (Pre-Deploy):** Run selectively. `pytest tests/integration/test_narrative_real.py`.
    *   *Scope:* Real Vertex AI calls, Redis round-trips.
*   **Golden Build Check:** Run `scripts/verify_governance_lobe.py` to smoke-test critical components.

---

## 2. Deployment Workflow

### A. The "Golden Image" Pipeline
1.  **Commit:** Code pushed to `main`.
2.  **Build:** Cloud Build triggers `cloudbuild.yaml`.
    *   Builds Python Agent image.
    *   Builds Go Dispatcher image.
    *   Builds Next.js Frontend image.
3.  **Push:** Images stored in Artifact Registry (`us-central1-docker.pkg.dev/muse-taia/smos-repo`).

### B. GKE Rollout
1.  **Config:** Update `infrastructure/k8s/env-config.yaml` (if needed).
2.  **Apply:** `kubectl apply -f infrastructure/k8s/`.
3.  **Restart:** `kubectl rollout restart deployment smos-backend`.

### C. "Warm Start" (Snapshot) Protocol
1.  **Boot:** The "Golden Pod" starts and initializes its `ContextCache` (loads the Bible).
2.  **Ready:** It hits `/internal/checkpoint-ready`.
3.  **Freeze:** The Go Dispatcher triggers a CRIU checkpoint via GKE API.
4.  **Scale:** New production jobs clone this checkpoint in milliseconds.

---

## 3. Production Workflows (The "Life" of the Muse)

### A. Proactive Trend Loop (Autonomous)
1.  **Scan:** `TrendScout` scrapes Reddit/TikTok (every hour).
2.  **Filter:** Calculates VVS. If > 50.0, generates an Intent.
3.  **Gate:** `CFOAgent` checks wallet balance. If solvent -> Proceed.
4.  **Plan:** `HLP` (RootAgent) creates a Task Graph.
5.  **Produce:** `WorkflowEngine` executes (Narrative -> Visual -> Motion).
6.  **QA:** `CriticAgent` validates output (<2% drift).
7.  **Publish:** (Simulated) Asset is staged for upload.

### B. Reactive Live Loop (Interactive)
1.  **Connect:** User connects via WebSocket to `/stream/muse-status`.
2.  **Listen:** `LiveApiService` streams audio to Gemini Multimodal.
3.  **Think:** `InteractiveRootAgent` updates internal thought stream.
4.  **Respond:** Gemini generates Audio response + Tool Calls (if needed).
5.  **Action:** `SwarmToolbox` executes tool (e.g. "Show me that image").

---

## 4. Emergency Protocols

*   **Financial Panic:** If `CFOAgent` detects `circuit_breaker_active`, all autonomous daemons are paused. Manual override required.
*   **Identity Collapse:** If `CriticAgent` rejects 5 consecutive generations, the system enters "Safe Mode" and falls back to a strict template workflow.
