# Track Plan: Genesis Pipeline & Studio Automation (Creation v2)

## Phase 1: Genesis Agent & DNA Generation
- [x] Task: Define Genesis DNA Schema 1aff81c
    - **Goal:** Create a Pydantic schema for the automated `dna.json` generation.
    - **Files:** `app/core/schemas/genesis.py`
- [x] Task: Implement GenesisAgent (The Inspirator) 9aeef75
    - **Goal:** Create an agent capable of 'Surprise Me' conceptualization and DNA drafting.
    - **Files:** `app/agents/genesis_agent.py`
- [x] Task: Conductor - User Manual Verification 'Genesis Logic' 9aeef75

## Phase 2: API & Storage Automation
- [x] Task: Implement /muses/surprise-me Endpoint 9aeef75
    - **Goal:** Return a random concept and a preview portrait URL.
    - **Files:** `app/main.py`
- [x] Task: Implement /muses/genesis Endpoint 9aeef75
    - **Goal:** Automate GCS storage of `face_master.png` and `dna.json` from the approved concept.
    - **Files:** `app/main.py`, `app/matrix/assets_manager.py`
- [x] Task: Unit Tests for Genesis Pipeline 9aeef75
    - **Goal:** Verify that a 'Surprise Me' call results in a valid GCS structure.
    - **Files:** `tests/test_genesis_pipeline.py`
- [x] Task: Conductor - User Manual Verification 'Full Genesis Flow' 9aeef75
