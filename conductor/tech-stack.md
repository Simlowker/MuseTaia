# SMOS v2 - Technical Stack & Infrastructure

**Status:** Golden Build (Production Ready)
**Date:** December 23, 2025

---

## 1. Core Frameworks & Languages

*   **Python 3.12+:** Primary language for AI Agents and Logic.
    *   *Reasoning:* Rich ecosystem for AI/ML (Pydantic, FastAPI, Google GenAI SDK).
*   **Go (Golang) 1.23+:** Infrastructure Dispatcher & High-Concurrency Networking.
    *   *Reasoning:* Low latency, efficient concurrency for handling thousands of job triggers.
*   **TypeScript / Next.js 15:** Frontend "Vitrine" and Dashboard.
    *   *Reasoning:* Reactive UI, Server-Side Rendering for SEO, strong typing.

## 2. Artificial Intelligence (The "Matrix")

*   **Google Gemini 3.0 Pro/Flash:** The cognitive engine (HLP, Narrative, Critic).
    *   *Role:* Reasoning, Context Caching, Multimodal Analysis.
*   **Google Imagen 3:** High-fidelity image generation.
    *   *Role:* Visual Virtuoso, Texture generation.
*   **Google Veo 3.1:** Cinematic video generation.
    *   *Role:* Director Agent (Motion).
*   **Vertex AI Context Caching:** Long-term memory persistence.
    *   *Role:* Storing the "Style Bible" and DNA with 7-day TTL to reduce latency and cost.

## 3. Infrastructure (The "Magic Factory")

*   **Google Kubernetes Engine (GKE) Autopilot:** Container orchestration.
    *   *Feature:* **Containerd Snapshots & CRIU**. Allows "Warm Start" of Python agents (cloning initialized memory) for <500ms cold starts.
*   **Google Artifact Registry:** Secure Docker image storage.
*   **Google Cloud Storage (GCS) FUSE:** Mounting heavy model weights and assets directly into Pods as a file system.
*   **Redis (Cloud Memorystore):** Real-time State Database (StateDB).
    *   *Role:* Shared memory for Agents (Mood, Wallet), Pub/Sub for SSE.
    *   *Resilience:* Configured with connection pooling and exponential backoff retries.

## 4. External Services

*   **Apify:** Social Media Scraping (Reddit, TikTok).
    *   *Role:* Providing real-world signals for the Trend Scout.
*   **ComfyUI (Self-Hosted on GKE):** Nodal image processing pipeline (optional advanced flow).
    *   *Role:* Fine-grained control over Inpainting/Outpainting and Identity preservation (PuLID).

## 5. Security & Governance

*   **Google Secret Manager:** Secure storage of API Keys and Tokens.
*   **Identity Aware Proxy (IAP):** Zero-trust access control for the Vitrine.
*   **CORS:** Restrictive policy allowing only whitelisted frontend domains.
*   **CFO Circuit Breaker:** Hard-coded financial limits preventing runaway API spending.

## 6. Testing Strategy

*   **Pytest:** Test runner.
*   **Unit Tests:** Mocked external services (Singleton `get_genai_client`).
*   **Integration Tests:** Real calls to Vertex AI/Redis (marked with `@pytest.mark.integration`).
