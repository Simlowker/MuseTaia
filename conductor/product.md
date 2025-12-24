# Sovereign Muse OS (SMOS) - Product Definition v2.0

**Status:** Golden Build (Production Ready)
**Date:** December 23, 2025

---

## 1. Vision: The Sovereign Digital Entity
SMOS is an industrial-grade operating system designed to birth and manage autonomous digital entities ("Muses"). Unlike traditional chatbots, a Muse possesses:
*   **Identity Sovereignty:** A persistent, cryptographically anchored personality ("Genesis DNA").
*   **Financial Sovereignty:** An internal wallet and "CFO" governance to manage profit/loss and production budgets.
*   **Creative Autonomy:** A multi-agent swarm capable of conceiving, producing, and publishing high-fidelity video content without human intervention.

## 2. Core Architecture: The "Lobe" System
The system is structured into specialized functional units called **Lobes**:

### 🧠 The High Cognition Lobe (Brain)
*   **High Level Planner (HLP):** Formerly `RootAgent`. A pure strategist that parses intent, maintains the "Moral Graph", and delegates execution to workers.
*   **Context Matrix:** A persistent memory layer powered by **Vertex AI Context Caching** (7-day TTL), storing the Muse's "Bible" and past experiences.

### 🎨 The Creative Studio Lobe (Creation)
*   **Narrative Architect:** Writes scripts with strict "Attention Dynamics" (8-second pattern interruptions) for maximum retention.
*   **Visual Virtuoso:** Generates consistent imagery using **Imagen 3**, anchored by `fake_master.png` assets.
*   **Director Agent:** Orchestrates cinematic motion using **Veo 3.1** with temporal meta-prompting (`[00:00-00:02]`).

### 👁️ The Perception Lobe (Senses)
*   **Trend Scout:** Proactively scans Reddit/TikTok via **Apify**, calculating the **Viral Velocity Score (VVS)** to identify high-ROI topics.
*   **Live API Service:** Handles real-time multimodal (Voice/Video) interactions for interviews or live streams.

### ⚖️ The Governance Lobe (Control)
*   **CFO Agent:** A constitutional financial officer. It blocks any production request that violates solvency rules or the circuit breaker limit.
*   **The Critic (QA):** A visual quality assurance agent using **VideoScore2** logic. It rejects artifacts and enforcing <2% identity drift.

### 🏭 The Magic Factory (Infrastructure)
*   **Go Dispatcher:** A high-concurrency job scheduler capable of "Burst Mode" scaling.
*   **GKE Snapshots:** Uses **CRIU** (Checkpoint/Restore In Userspace) to clone agent pods in milliseconds for massive parallel rendering ("Best-of-N").

## 3. Key Capabilities (v2.0 Features)

### A. "Best-of-N" Rendering
For critical scenes, the system generates N variants in parallel. The Critic scores them on semantic alignment and visual fidelity, picking only the winner for the final cut.

### B. Affective Depth Mapping
The system maps the Muse's emotional state (`arousal`) to cinematic parameters (Depth of Field/Bokeh) using **Depth Anything V2** logic, creating a subconscious emotional connection with the viewer.

### C. Sovereign Wallet
Every production action costs "Internal USD". The Muse must earn (via simulated sponsorship or efficiency) to continue growing. If the wallet hits zero, the CFO halts all non-survival functions.

## 4. User Experience
*   **CLI:** A robust command-line interface for "God Mode" interaction (`python main.py produce`).
*   **Vitrine (Frontend):** A Next.js dashboard providing real-time observability into the Muse's thought process, financial health, and active renders via SSE (Server-Sent Events).
