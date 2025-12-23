# Track Plan: Sovereign Talk (Interactive Orchestration)

## Phase 1: Interactive Toolset (The Muse's Hands)
- [ ] Task: Wrap Swarm Agents as Executable Tools
    - **Goal:** Standardize Narrative, Visual, and Search agents into a format that the Gemini Live API can call as functions.
    - **Files:** `app/agents/tools/swarm_tools.py`
    - **Tech:** Google GenAI Tool Use.
    - **Tests:** Verify tool definitions and mock execution.
- [ ] Task: Implement Live Tool Dispatcher
    - **Goal:** Create a handler that executes swarm tasks in response to model function calls during a live session.
    - **Files:** `app/core/services/live_api.py` (update).
- [ ] Task: Conductor - User Manual Verification 'Interactive Toolset' (Protocol in workflow.md)

## Phase 2: Live Persona & Context (The Muse's Soul)
- [ ] Task: Integrate Identity Context (Caching) into Live Session
    - **Goal:** Ensure the live session starts with the Muse's full DNA context (1M+ tokens).
    - **Files:** `app/core/services/live_api.py` (update).
    - **Tech:** Vertex AI Context Caching.
- [ ] Task: Implement Signature Voice & Audio Config
    - **Goal:** Configure the Live API with the Muse's vocal personality.
    - **Files:** `app/core/services/live_api.py` (update).
- [ ] Task: Conductor - User Manual Verification 'Live Persona' (Protocol in workflow.md)

## Phase 3: Real-time Brain (The RootAgent Loop)
- [ ] Task: Implement Interactive RootAgent Handler
    - **Goal:** Manage the state of the conversation, updating Mood and Thoughts in Redis as the dialogue progresses.
    - **Files:** `app/agents/interactive_root.py`
    - **Tech:** Asyncio, StateDB.
- [ ] Task: Implement Background Task Orchestration
    - **Goal:** Allow the Muse to "hand off" heavy tasks (like video rendering) to the ACE factory without breaking the conversation flow.
    - **Files:** `app/core/workflow_engine.py` (update).
- [ ] Task: Conductor - User Manual Verification 'Real-time Brain' (Protocol in workflow.md)

## Phase 4: Low-Latency Studio Interaction
- [ ] Task: End-to-End Voice Scenario Test
    - **Goal:** Verify the full flow: "Human Voice -> RootAgent Tool Call (Visual) -> Critic Validation -> Voice Response".
    - **Files:** `tests/test_sovereign_talk_flow.py`
- [ ] Task: Conductor - User Manual Verification 'Low-Latency Interaction' (Protocol in workflow.md)
