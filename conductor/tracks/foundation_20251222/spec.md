# Track Specification: Build the Phase 1 Foundation: Socle ADK & Matrix Identity

## Overview
This track establishes the core infrastructure for the Sovereign Muse OS (SMOS). The primary goal is to build the "Brain" (ADK Orchestration) and the "Soul" (Matrix Identity) of the system. This foundation will support the multi-agent swarm, ensuring all future content generation is anchored in a persistent, sovereign identity.

## Goals
1.  **Establish the ADK "Mission Control":** Implement the RootAgent using the Google Agent Development Kit (ADK) to manage swarm communication and the "Single-Master Protocol".
2.  **Implement "The Matrix" (Identity Anchor):** Deploy Vertex AI Context Caching to store the Muse's "Genesis DNA" (Backstory, Voice, Moral Graph) and integrate with Google Cloud Storage for "Signature Assets".
3.  **Deploy the Genesis StateDB:** Set up a Redis-based real-time database to track the Muse's "Mood" and "Wallet" state, enabling synchronized "consciousness" across the swarm.
4.  **Implement "The Critic" (v1):** Create a baseline QA agent using Gemini 3 Vision to validate visual consistency against the Signature Assets.

## Key Features

### 1. RootAgent Orchestration (ADK)
-   **Technology:** Google ADK (Python), FastAPI.
-   **Function:** Acts as the central nervous system.
-   **Capabilities:**
    -   Receives high-level intent from the user (Single-Master Protocol).
    -   Decomposes tasks using parallel function calling.
    -   Routes commands to specialized agents (CSO, EIC) via gRPC/FastAPI.
    -   Enforces "Identity Injection" (Moral Graph, Tone) in every request.

### 2. "The Matrix" Memory System
-   **Technology:** Vertex AI Context Caching, Google Cloud Storage (GCS).
-   **Components:**
    -   **Context Cache:** Stores 1M+ tokens of static DNA (Backstory, Personality, Voice Guidelines).
    -   **Signature Assets DB (GCS):** Stores versioned reference images (Face, Profile, Style) and "Visual Muscle Memory" (Seeds, Depth Maps).
    -   **Access Layer:** A Python module to retrieve context and assets with <50ms latency.

### 3. Shared StateDB (Redis)
-   **Technology:** Redis.
-   **Function:** Real-time state management.
-   **Schema:**
    -   `muse:mood`: JSON object defining current emotional vector (e.g., `{"valence": 0.8, "arousal": 0.6}`).
    -   `muse:wallet`: JSON object tracking financial autonomy (e.g., `{"credits": 5000, "revenue": 120}`).
    -   `muse:world`: JSON object tracking physical location and object states.

### 4. The Critic v1 (Visual QA)
-   **Technology:** Gemini 3 Vision, Python.
-   **Function:** Automated visual validation.
-   **Logic:**
    -   Accepts a generated image and a set of "Reference Assets".
    -   Computes visual similarity (target >98%).
    -   Returns `Pass/Fail` with a structured "Drift Report".

## User Stories
1.  **Genesis of the Muse:** As a user, I want to define and store the Muse's core DNA so she remains consistent from Day 0.
2.  **Swarm Communication:** As a developer, I want agents to exchange structured JSON orders via ADK to ensure reliable coordination.
3.  **State Awareness:** As a system, I want all agents to access real-time Mood and Wallet data to synchronize the Muse's behavior.
4.  **Visual Gatekeeping:** As a user, I want a QA agent to automatically reject content that deviates from the Muse's visual identity.

## Non-Functional Requirements
-   **Latency:** Agent-to-agent communication < 50ms.
-   **Consistency:** Visual similarity score > 98%.
-   **Test Coverage:** > 90% for all core modules.
