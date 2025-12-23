# SMOS v2 Technical Stack (Industrial & Sovereign)

## 🧠 Lobe de Haute Cognition (The Brain)
- **Framework:** Google ADK (Agent Development Kit).
- **Core LLM:** Gemini 3.0 Pro & Flash (Vertex AI).
- **Memory:** Vertex AI Context Caching (1M+ tokens) + Redis (Shared State).
- **Orchestration:** TaskGraphRunner (Sequential & Parallel nodes).

## 🛰️ Lobe de Perception (The Scout)
- **Trend Discovery:** TrendScout with Viral Velocity Score (VVS) algorithm.
- **Data Source:** Reddit/TikTok via ApifyClientAsync.
- **Grounding:** Google Search Grounding (Vertex AI).

## 🎨 Lobe de Création (The Creative Studio)
- **Identity Lock:** PuLID + IP-Adapter FaceID via ComfyScript.
- **Image Gen:** Imagen 3 (Vertex AI).
- **Video Gen:** Veo 3.1 (Google DeepMind).
- **Audio Gen:** Google Cloud Text-to-Speech (Studio Voices).
- **Sync:** LipSync Pipeline (LivePortrait/SadTalker on GKE GPU).

## ⚖️ Lobe de Gouvernance (Forge Control)
- **Financial Officer:** CFOAgent with constitutional Circuit Breakers.
- **Quality Assurance:** The Critic (2% Deviation Rule via Biometric Comparison).
- **Ledger:** Transaction history stored in Redis.

## 🏗️ Infrastructure (The Magic Factory)
- **Orchestrator:** Google Kubernetes Engine (GKE).
- **Acceleration:** GKE Pod Snapshots (CRIU) for 2.4s boot time.
- **Compute:** NVIDIA L4 GPU Node Pools.
- **Storage:** Google Cloud Storage (GCS) with GCS FUSE mounting.
- **Dispatcher:** High-concurrency Golang Dispatcher.