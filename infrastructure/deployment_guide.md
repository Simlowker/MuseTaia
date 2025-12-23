# SMOS v2 - GCP Deployment Guide

This document outlines the infrastructure requirements for deploying Sovereign Muse OS v2 on Google Cloud Platform.

## 1. Prerequisites
- **Google Cloud SDK (`gcloud`)**: Must be installed and authenticated (`gcloud auth login`).
- **Project**: A GCP Project with billing enabled.

## 2. API Configuration (Automated)
Run the provided script to enable all necessary services:
```bash
cd infrastructure
chmod +x setup_gcp.sh
./setup_gcp.sh
```

## 3. Quota Increases (Manual Implementation)
Go to **IAM & Admin > Quotas & System Limits** in the GCP Console and ensure:

### Compute Engine API
| Metric | Region | Required Limit | Reason |
|--------|--------|----------------|--------|
| **NVIDIA L4 GPUs** | `us-central1` | **1+** | Creative Studio rendering |

### Vertex AI API
| Metric | Limit Name | Required | Reason |
|--------|------------|----------|--------|
| **Imagen 3** | `Predict Requests per minute` | **Standard** | Image Generation |
| **Veo 3.1** | `Predict Requests per minute` | **Standard** | Video Generation |

> **Note**: Verify "Context Caching" is enabled for Gemini 1.5 Pro.

### ⚠️ Troubleshooting Quotas
**Button "Edit Quotas" greyed out?**
If you cannot request a quota increase, it is likely because you are on the **GCP Free Trial**.
1.  Click the **"Activate"** (Activer) button in the top-right of the console header to upgrade to a full account.
2.  *Note: You keep your free credits, but this unlocks GPU access.*
3.  Refresh the page and try editing the quota again.

**Check Quotas via CLI:**
Run this in Cloud Shell to see your current limit:
```bash
gcloud compute regions describe us-central1 --format="value(quotas.metric,quotas.limit)" | grep NVIDIA_L4
```

## 4. GKE Cluster Setup (Dashboard)
When creating your cluster in **Kubernetes Engine**:

1.  **Region**: Select `us-central1`.
2.  **Node Pool**:
    *   **Machine Type**: `g2-standard-8` (4 vCPUs, 16GB RAM, 1x NVIDIA L4).
    *   **Image Type**: `Container-Optimized OS with containerd` (or Ubuntu with containerd).
3.  **Features**:
    *   [x] **Enable GCS FUSE CSI Driver** (Critical for model assets).
    *   [x] **Enable NVIDIA GPU Device Plugin** (Critical for GPU access).
    *   [x] **Enable CRIU / Pod Checkpointing** (If available/required).

## 5. Deployment
Apply the Kubernetes manifests:
```bash
```

## 5. Deployment Pipeline (Cloud Shell)

Since `gcloud` is not on your local machine, we will use **GitHub + Cloud Shell**.

### Step A: Push Code
1. Commit all changes locally:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

### Step B: Clone & Deploy in Cloud Shell
Switch to your Google Cloud Shell window:

1. **Clone the repo** (Public):
   ```bash
   git clone https://github.com/Simlowker/MuseTaia.git
   cd MuseTaia
   ```

2. **Trigger Build & Deploy**:
   ```bash
   gcloud builds submit --config=cloudbuild.yaml .
   ```

## 6. Architecture Confirmation
**Can I run this on CPU?**
YES.
- **Frontend**: Runs on Next.js (CPU).
- **Backend**: Runs on Python/FastAPI (CPU).
- **AI Generation**: Uses remote Google APIs (Vertex AI), so no local GPU is needed.
- **Database**: Redis/Postgres run perfectly on standard CPUs.

**Conclusion**: The CPU-only cluster (`e2-standard-4`) is fully capable of running the entire SMOS v2 production stack.
