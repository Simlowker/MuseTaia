# Sovereign Muse OS (SMOS) v2

Autonomous Content Engine (ACE) - Multi-Agent Swarm for High-Fidelity Digital Entities.

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.13+**
- **Node.js 18+**
- **Docker & Docker Compose**
- **Google Cloud Project** with Vertex AI, Imagen 3, and GCS enabled.

### 2. Infrastructure Setup
Launch the StateDB (Redis):
```bash
docker-compose up -d redis
```

### 3. Environment Configuration
Create your `.env` (Backend) and `frontend/.env.local` based on the provided `.example` files.

### 4. System Bootstrap
Initialize the Muse's DNA and first MoodState:
```bash
PYTHONPATH=. .venv/bin/python3 scripts/bootstrap_system.py
```

### 5. Launch the Swarm (Backend)
```bash
uvicorn app.main:app --reload
```

### 6. Launch the Heart (Frontend)
```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to enter the Sovereign Heart.

## 🏛️ System Architecture
- **RootAgent (Gemini 3.0 Flash):** Real-time orchestration and conversation.
- **The Swarm:** Narrative Lead, Visual Virtuoso (Imagen 3), Motion Engineer (Veo 3.1).
- **The Critic:** Surgical QA and visual consistency guard.
- **The Matrix:** Vertex AI Context Caching (1M+ tokens) + GCS Signature Assets.
- **The Forge:** Industrial GKE rendering factory.

---
*Identity Anchor: Genesis_v1 verified.*
