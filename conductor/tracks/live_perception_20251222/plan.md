# Track Plan: Live Perception (Multimodal Live API)

## Phase 1: Live API Foundation (The Nervous System)
- [x] Task: Implement Live API Service Wrapper
    - **Goal:** Create a service to manage WebSocket connections to the Gemini Multimodal Live API.
    - **Files:** `app/core/services/live_api.py`
    - **Tech:** WebSockets, Gemini Multimodal Live API.
    - **Tests:** Verify connection and basic message exchange.
- [ ] Task: Conductor - User Manual Verification 'Live API Foundation' (Protocol in workflow.md)

## Phase 2: Sensory Handlers (Vision & Audio)
- [x] Task: Implement Video Stream Handler
    - **Goal:** Process real-time video frames and extract visual descriptions.
    - **Files:** `app/agents/handlers/visual_stream.py`
    - **Tech:** Gemini 3 Flash.
    - **Tests:** Mock video stream and verify visual summary generation.
- [x] Task: Implement Audio/Voice Handler
    - **Goal:** Process real-time audio for speech-to-text and intent parsing.
    - **Files:** `app/agents/handlers/audio_stream.py`
    - **Tech:** Gemini Multimodal Live (Audio).
- [ ] Task: Conductor - User Manual Verification 'Sensory Handlers' (Protocol in workflow.md)

## Phase 3: Proactive Reaction Loop (The Reflex)
- [x] Task: Integrate Live Perception with RootAgent
    - **Goal:** Enable the RootAgent to receive sensory alerts and update the Muse's "Current Thought" in real-time.
    - **Files:** `app/agents/root_agent.py` (update), `app/core/scheduler.py` (update).
    - **Tech:** Asyncio, StateDB.
    - **Tests:** Simulate a visual stimulus (e.g., "A new fashion trend appeared on screen") and verify RootAgent reaction.
- [ ] Task: Conductor - User Manual Verification 'Proactive Reaction Loop' (Protocol in workflow.md)

## Phase 4: Low-Latency Integration
- [ ] Task: Implement End-to-End Live Interaction Pipeline
    - **Goal:** Verify the system can perceive a live event, update internal state, and suggest a "Creative Studio" action within seconds.
    - **Files:** `tests/test_live_perception_flow.py`
    - **Tests:** Integration test from live input to orchestrator dispatch.
- [ ] Task: Conductor - User Manual Verification 'Low-Latency Integration' (Protocol in workflow.md)
