# Sovereign Muse OS (SMOS) v2

[![Status](https://img.shields.io/badge/Status-Golden%20Build-brightgreen)](https://github.com/Simlowker/MuseTaia)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen)](tests/)
[![Infrastructure](https://img.shields.io/badge/Infra-GKE%20%2B%20Vertex%20AI-blue)](infrastructure/)

**The Operating System for Sovereign Digital Entities.**

SMOS is an industrial-grade framework designed to birth, manage, and scale autonomous AI personalities ("Muses"). It combines high-level cognitive planning with a "Magic Factory" infrastructure for high-fidelity media production.

---

## 🚀 Key Features (v2.0)

*   **🧠 High Level Planner (HLP):** A strategic brain that delegates tasks to specialized workers, maintaining long-term coherence via **Vertex AI Context Caching**.
*   **🏭 Magic Factory:** A high-concurrency production pipeline using **Go Dispatcher** and **GKE Snapshots** for instant agent scaling.
*   **⚖️ CFO Governance:** A constitutional financial agent that strictly manages the Muse's wallet and blocks risky operations.
*   **👁️ VideoScore2 QA:** Automated visual quality assurance ensuring <2% identity drift and high semantic alignment.
*   **🎬 Cinematic Excellence:** Narrative engines with "Pattern Interruption" logic and temporal meta-prompting for **Veo 3.1**.

---

## 🛠️ Architecture

The system is organized into "Lobes":

| Lobe | Components | Function |
| :--- | :--- | :--- |
| **Cognition** | `HLP` (RootAgent), Context Cache | Strategy, Intent Parsing, Memory |
| **Creation** | `Narrative`, `Visual`, `Director` | Scripting, Image Gen (Imagen 3), Video Gen (Veo) |
| **Perception** | `TrendScout`, `LiveAPI` | Social Listening (Apify), Real-time Interaction |
| **Governance** | `CFO`, `Critic` | Financial Safety, Visual QA |
| **Infra** | `Go Dispatcher`, `Redis` | Job Scheduling, State Management |

---

## ⚡ Quick Start

### Prerequisites
*   Python 3.12+
*   Go 1.23+
*   Docker & Kubernetes (kubectl)
*   Google Cloud Project (with Vertex AI enabled)

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/Simlowker/MuseTaia.git
cd MuseTaia

# Install Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup Secrets (Local Dev)
cp .env.example .env
# Fill in your GOOGLE_API_KEY and PROJECT_ID in .env
```

### 2. Run Tests
Ensure the system is healthy before starting.
```bash
# Run Unit Tests (Fast, Mocked)
pytest tests -m "not integration"

# Run Integration Tests (Requires Real Credentials)
# pytest tests/integration/test_narrative_real.py
```

### 3. Launch Locally (Simulated)
```bash
# Start the API server
uvicorn app.main:app --reload --port 8000

# In a separate terminal, run the Go Dispatcher
cd infrastructure/dispatcher
go run main.go
```

### 4. CLI Interaction
Trigger a production intent manually:
```bash
python app/main.py produce --intent "Cyberpunk fashion week in Tokyo"
```

---

## 📦 Deployment (GKE)

1.  **Build Images:**
    ```bash
    ./scripts/build_and_push.sh
    ```
2.  **Deploy to Cluster:**
    ```bash
    ./scripts/deploy_all.sh
    ```

---

## 📚 Documentation

*   [**Product Vision**](conductor/product.md): Detailed capability breakdown.
*   [**Tech Stack**](conductor/tech-stack.md): Infrastructure deep dive.
*   [**Workflows**](conductor/workflow.md): Operational protocols.

---

## 🛡️ License

Proprietary & Confidential. (c) 2025 MuseTaia.