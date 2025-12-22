# Track Plan: Perception & Grounding (TrendScanner & Search)

## Phase 1: Search Infrastructure (The Sensors)
- [x] Task: Implement Search Service Wrapper
    - **Goal:** Create a unified interface for agents to perform web searches using Google Search.
    - **Files:** `app/core/services/search_service.py`
    - **Tech:** Google GenAI Tooling (Google Search).
    - **Tests:** Verify search queries return structured results.
- [ ] Task: Conductor - User Manual Verification 'Search Infrastructure' (Protocol in workflow.md)

## Phase 2: TrendScanner Agent (The Analyst)
- [x] Task: Define TrendReport Schema
    - **Goal:** Standardize the output for analyzed trends.
    - **Files:** `app/core/schemas/trend.py`
    - **Tech:** Pydantic.
- [x] Task: Implement TrendScanner Agent
    - **Goal:** Create an agent that takes a topic, searches for real-time context, and evaluates it against the Muse's "Moral Graph" and Persona.
    - **Files:** `app/agents/trend_scanner.py`
    - **Tech:** Gemini 3 Flash (for speed/analysis), Search Service.
    - **Tests:** Verify analysis of "hot" topics vs "blocked" topics.
- [ ] Task: Conductor - User Manual Verification 'TrendScanner Agent' (Protocol in workflow.md)

## Phase 3: Proactive Triggering (The Spark)
- [x] Task: Implement Proactive Orchestration Loop
    - **Goal:** Enable the system to autonomously scan a list of interests and trigger production if a high-value trend is found.
    - **Files:** `app/core/scheduler.py` or update `app/core/workflow_engine.py`.
    - **Tech:** Python, Asyncio.
    - **Tests:** Simulate a high-score trend triggering the `produce_video_content` flow.
- [ ] Task: Conductor - User Manual Verification 'Proactive Triggering' (Protocol in workflow.md)

## Phase 4: Cultural Grounding (Narrative Enhancement)
- [ ] Task: Update Narrative Agent with Search Grounding
    - **Goal:** Allow the Narrative Agent to verify slang and references before finalizing a script.
    - **Files:** `app/agents/narrative_agent.py`
    - **Tech:** Gemini Tool Use (Search).
    - **Tests:** Verify script adjustments based on search data (e.g., correcting a date or term).
- [ ] Task: Conductor - User Manual Verification 'Cultural Grounding' (Protocol in workflow.md)
