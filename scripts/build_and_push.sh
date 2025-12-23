#!/bin/bash

# SMOS v2 - Build and Push Script
# Purpose: Compile and push Docker images to Google Artifact Registry

set -e

PROJECT_ID="muse-taia"
REGION="us-central1"
REPO_NAME="smos-repo" # Created via setup_gcp.sh

IMAGE_AGENT="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/smos-agent:latest"
IMAGE_DISPATCHER="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/smos-dispatcher:latest"

echo "📦 Starting SMOS v2 Build Pipeline..."

# 1. AUTHENTICATION
echo "🔐 Authenticating with Artifact Registry..."
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

# 2. BUILD AGENTS (Python)
echo "🛸 Building SMOS Swarm Agent Image..."
docker build -t $IMAGE_AGENT .

# 3. BUILD DISPATCHER (Go)
echo "⚙️ Building SMOS Dispatcher Image..."
cd infrastructure/dispatcher
docker build -t $IMAGE_DISPATCHER .
cd ../..

# 4. PUSH IMAGES
echo "🚀 Pushing images to Artifact Registry..."
docker push $IMAGE_AGENT
docker push $IMAGE_DISPATCHER

echo ""
echo "✅ BUILD & PUSH COMPLETE"
echo "--------------------------------------------------"
echo "Agent Image:      $IMAGE_AGENT"
echo "Dispatcher Image: $IMAGE_DISPATCHER"
echo "--------------------------------------------------"
echo "You can now run ./scripts/deploy_all.sh to update the GKE cluster."
