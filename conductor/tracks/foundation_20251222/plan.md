# Track Plan: Build the Phase 1 Foundation: Socle ADK & Matrix Identity

## Phase 1: Infrastructure Setup & Project Skeleton
- [ ] Task: Initialize Project Structure & Dependency Management
    - **Goal:** Create the standard Python project layout and install core dependencies.
    - **Files:** `pyproject.toml`, `requirements.txt`, `app/`, `tests/`
    - **Tech:** Python, Poetry/Pip
    - **Tests:** Verify environment setup and import capabilities.
- [ ] Task: Configure Google Cloud & Vertex AI Environment
    - **Goal:** Set up authentication and connection to Google Cloud Platform (Vertex AI, GCS).
    - **Files:** `app/core/config.py`, `.env` (template)
    - **Tech:** Google Cloud SDK, Pydantic
    - **Tests:** Verify successful authentication and API connectivity.
- [ ] Task: Set up Redis Infrastructure (StateDB)
    - **Goal:** Configure Redis connection for real-time state management.
    - **Files:** `app/core/redis_client.py`
    - **Tech:** Redis, redis-py
    - **Tests:** Verify connection, set/get operations, and latency.
- [ ] Task: Conductor - User Manual Verification 'Infrastructure Setup & Project Skeleton' (Protocol in workflow.md)

## Phase 2: "The Matrix" Memory Implementation
- [ ] Task: Implement Signature Assets Manager (GCS)
    - **Goal:** Create a module to upload, retrieve, and version "Signature Assets" (images, seeds).
    - **Files:** `app/matrix/assets_manager.py`
    - **Tech:** Google Cloud Storage Client
    - **Tests:** Test upload, retrieval, versioning, and metadata access.
- [ ] Task: Implement Vertex AI Context Caching Layer
    - **Goal:** Create the interface for managing long-context memory (Backstory, Voice).
    - **Files:** `app/matrix/context_cache.py`
    - **Tech:** Vertex AI SDK
    - **Tests:** Test cache creation, retrieval, and expiration handling.
- [ ] Task: Define "Genesis DNA" Schema & Loader
    - **Goal:** Define the JSON schema for the Muse's identity and create a loader to populate the Context Cache.
    - **Files:** `app/matrix/models.py`, `app/matrix/dna_loader.py`
    - **Tech:** Pydantic
    - **Tests:** Validate schema integrity and successful data loading.
- [ ] Task: Conductor - User Manual Verification '"The Matrix" Memory Implementation' (Protocol in workflow.md)

## Phase 3: RootAgent & ADK Orchestration
- [ ] Task: Initialize RootAgent with Google ADK
    - **Goal:** Create the basic RootAgent using the Agent Development Kit framework.
    - **Files:** `app/agents/root_agent.py`
    - **Tech:** Google ADK
    - **Tests:** Verify agent initialization and basic "ping" response.
- [ ] Task: Implement Single-Master Protocol (Intent Parsing)
    - **Goal:** Enable the RootAgent to parse high-level user commands and identify the "Master" source (Human vs. Community).
    - **Files:** `app/agents/protocols/master_sync.py`
    - **Tech:** Gemini 3 Flash (Mocked for now or live)
    - **Tests:** Test parsing of various command structures and master identification.
- [ ] Task: Implement Parallel Function Calling Mechanism
    - **Goal:** Configure the RootAgent to decompose tasks and prepare structured orders for sub-agents.
    - **Files:** `app/agents/orchestrator.py`
    - **Tech:** Google ADK, Python
    - **Tests:** Verify that complex tasks are correctly broken down into sub-task definitions.
- [ ] Task: Conductor - User Manual Verification 'RootAgent & ADK Orchestration' (Protocol in workflow.md)

## Phase 4: Shared State & The Critic v1
- [ ] Task: Implement StateDB Access Layer (Mood & Wallet)
    - **Goal:** Create a structured API for agents to read/write the Muse's real-time state.
    - **Files:** `app/state/db_access.py`, `app/state/models.py`
    - **Tech:** Redis, Pydantic
    - **Tests:** Test concurrent read/write access and schema validation for Mood/Wallet objects.
- [ ] Task: Implement "The Critic" v1 (Visual QA Agent)
    - **Goal:** Build the initial logic for visual consistency checking using Gemini 3 Vision.
    - **Files:** `app/agents/critic_agent.py`
    - **Tech:** Gemini 3 Vision API
    - **Tests:** Test image comparison logic (mocked images) and drift reporting.
- [ ] Task: Conductor - User Manual Verification 'Shared State & The Critic v1' (Protocol in workflow.md)
