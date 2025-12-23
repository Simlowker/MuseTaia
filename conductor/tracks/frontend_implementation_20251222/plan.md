# Track Plan: Sovereign Frontend (Sovereign Minimalism 2.0)

## Phase 1: Environment Setup & Core Shell [checkpoint: 5b4bcd7]
- [x] Task: Initialize Next.js Project
    - **Goal:** Set up the frontend project structure with TypeScript and Bootstrap CSS.
    - **Files:** `frontend/`, `frontend/package.json`
    - **Tech:** Next.js, Bootstrap 5, Material Design components.
- [x] Task: Implement Glassmorphism Layout (Sovereign Shell)
    - **Goal:** Create the core layout with Z-index layers and the dynamic mood-based color provider.
    - **Files:** `frontend/src/components/Layout.tsx`, `frontend/src/context/MoodContext.tsx`
    - **Tech:** CSS Modules, React Context.
- [x] Task: Conductor - User Manual Verification 'Core Shell' (Protocol in workflow.md) 5b4bcd7

## Phase 2: The Sovereign Heart (Command Center)
- [ ] Task: Implement Central Visual Vortex & Waveform
    - **Goal:** Build the main video area (Veo 3.1 placeholder) and the reactive neural waveform.
    - **Files:** `frontend/components/VisualVortex.tsx`, `frontend/components/NeuralWaveform.tsx`
- [ ] Task: Build Cognition & Swarm Sidebars
    - **Goal:** Implement the Trends Feed (left) and Swarm Status/Instant Canvas (right).
    - **Files:** `frontend/components/TrendFeed.tsx`, `frontend/components/SwarmStatus.tsx`
- [ ] Task: Conductor - User Manual Verification 'Sovereign Heart' (Protocol in workflow.md)

## Phase 3: The Forge & DNA Matrix
- [ ] Task: Implement Production Timeline & Critic Dashboard
    - **Goal:** Build the Gantt-style timeline and the Drift Visualizer tool.
    - **Files:** `frontend/pages/forge.tsx`, `frontend/components/DriftVisualizer.tsx`
- [ ] Task: Build DNA Architect & Vault
    - **Goal:** Create the visual editor for the Moral Graph and the high-res GCS asset gallery.
    - **Files:** `frontend/pages/matrix.tsx`, `frontend/components/DNAEditor.tsx`
- [ ] Task: Conductor - User Manual Verification 'Forge & Matrix' (Protocol in workflow.md)

## Phase 4: Ledger & Master Control
- [ ] Task: Implement Financial Ledger & Sync Controller
    - **Goal:** Build the ROI/Cost dashboard and the Master Sync (Human vs Community) toggle.
    - **Files:** `frontend/pages/ledger.tsx`, `frontend/components/MasterSync.tsx`
- [ ] Task: End-to-End API Integration
    - **Goal:** Connect all frontend components to the existing Python Backend (StateDB, WorkflowEngine).
    - **Files:** `frontend/services/api.ts`
- [ ] Task: Conductor - User Manual Verification 'Frontend Completion' (Protocol in workflow.md)
