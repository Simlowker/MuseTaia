#!/bin/bash

# SMOS v2 - Google Cloud Platform Setup Script
# Purpose: Activate APIs and prepare environment for Industrial Swarm

set -e

PROJECT_ID="muse-taia"
REGION="us-central1"

echo "🌌 Initializing SMOS v2 Environment on Project: $PROJECT_ID"

# 1. Set Project
gcloud config set project $PROJECT_ID

# 2. Enable Required Services
echo "🛡️ Activating Google Cloud APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    compute.googleapis.com \
    container.googleapis.com \
    storage.googleapis.com \
    texttospeech.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    iam.googleapis.com \
    notebooks.googleapis.com

# 3. Create Artifact Registry for Docker Images
echo "📦 Creating Artifact Registry..."
if ! gcloud artifacts repositories describe smos-repo --location=$REGION &>/dev/null; then
    gcloud artifacts repositories create smos-repo \
        --repository-format=docker \
        --location=$REGION \
        --description="SMOS v2 Agent Images"
else
    echo "-> Repository already exists."
fi

# 4. Create GCS Bucket for Assets
echo "🗄️ Creating GCS Bucket..."
if ! gsutil ls -b gs://smos-assets &>/dev/null; then
    gsutil mb -l $REGION gs://smos-assets
else
    echo "-> Bucket already exists."
fi

# 5. Summary & Quotas
echo ""
echo "✅ CORE APIs ACTIVATED"
echo "--------------------------------------------------"
echo "⚠️  ACTION REQUIRED: CHECK YOUR QUOTAS"
echo "1. Go to: https://console.cloud.google.com/iam-admin/quotas"
echo "2. Filter by: 'NVIDIA L4 GPUs' in $REGION"
echo "3. Ensure 'Limit' is at least 1."
echo "--------------------------------------------------"
echo "🚀 Your project is now ready for GKE deployment."
