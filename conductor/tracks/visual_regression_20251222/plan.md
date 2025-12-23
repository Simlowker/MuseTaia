# Track Plan: Visual Regression Suite (Identity Anchors)

## Phase 1: Genesis Anchor Registry
- [x] Task: Define Identity Anchor Schema
    - **Goal:** Standardize how "Day 0" reference assets and their embeddings are stored.
    - **Files:** `app/matrix/models.py` (update), `app/matrix/anchors.py`
    - **Tech:** Pydantic, GCS.
    - **Tests:** Validate anchor objects and retrieval.
- [x] Task: Implement Anchor Management Utility
    - **Goal:** Provide methods to register and retrieve the "Genesis" reference frames.
    - **Files:** `app/matrix/assets_manager.py` (update).
    - **Tech:** Python, GCS.
- [ ] Task: Conductor - User Manual Verification 'Genesis Anchor Registry' (Protocol in workflow.md)

## Phase 2: Similarity Analysis Engine
- [x] Task: Implement Multimodal Similarity Module
    - **Goal:** Use Gemini 3 Vision to compare a new render against the Identity Anchor.
    - **Files:** `app/core/utils/visual_comparison.py`
    - **Tech:** Gemini 3.0 Flash Preview (Vision).
    - **Tests:** Verify score generation for matching vs. different faces.
- [x] Task: Implement Structural Similarity (SSIM) Fallback
    - **Goal:** Add pixel-level structural comparison for background consistency.
    - **Files:** `app/core/utils/visual_comparison.py`
    - **Tech:** Pillow/NumPy or specialized library.
    - **Tests:** Verify score for identical vs different images.
- [ ] Task: Conductor - User Manual Verification 'Similarity Analysis' (Protocol in workflow.md)

## Phase 3: Regression Test Runner
- [x] Task: Create Automated Regression Script
    - **Goal:** A CLI tool that triggers a sample generation and runs the comparison.
    - **Files:** `scripts/run_visual_regression.py`
    - **Tech:** Python.
- [x] Task: Implement Pass/Fail Threshold Logic
    - **Goal:** Enforce the "2% Deviation" rule from the workflow guidelines.
    - **Files:** `scripts/run_visual_regression.py`
    - **Tests:** Verify CLI exit codes for pass/fail scenarios.
- [ ] Task: Conductor - User Manual Verification 'Regression Test Runner' (Protocol in workflow.md)

## Phase 4: CI/CD Integration
- [ ] Task: Integrate Regression Suite into Cloud Build
    - **Goal:** Ensure the build fails if the visual identity drifts during updates.
    - **Files:** `cloudbuild.yaml` (update).
- [ ] Task: Conductor - User Manual Verification 'CI/CD Integration' (Protocol in workflow.md)
