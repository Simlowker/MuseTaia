#!/bin/bash

# SMOS v2 Industrial Deployment Script
# Purpose: Full infrastructure setup on GKE with environment synchronization

set -e

PROJECT_ID="muse-taia"
CLUSTER_NAME="smos-v2-cluster"
REGION="us-central1"

echo "🌌 Starting SMOS v2 Deployment for Project: $PROJECT_ID"

# 1. AUTHENTICATION
echo "🔐 Verifying GCP Authentication..."
gcloud config set project $PROJECT_ID
gcloud auth configure-docker --quiet

# 2. INFRASTRUCTURE SETUP
echo "🏗️ Creating Node Pool for Visual Studio (GPU L4 + CRIU)..."
# (Vérifier si le pool existe déjà pour éviter l'erreur)
if ! gcloud container node-pools describe smos-visual-lobe-pool --cluster $CLUSTER_NAME --region $REGION &>/dev/null; then
    gcloud container node-pools create smos-visual-lobe-pool \
        --cluster $CLUSTER_NAME \
        --region $REGION \
        --machine-type g2-standard-8 \
        --accelerator type=nvidia-l4,count=1 \
        --image-type UBUNTU_CONTAINERD \
        --num-nodes 1 \
        --min-nodes 1 --max-nodes 10 --enable-autoscaling \
        --node-labels=runtime=criu-enabled,lobe=creative-studio \
        --metadata=install-criu=true
else
    echo "-> Node Pool already exists."
fi

# 3. ENVIRONMENT & SECRETS
echo "🔑 Injecting Secrets and ConfigMaps..."
kubectl apply -f infrastructure/k8s/env-config.yaml

# 4. RUNTIME & SERVICES
echo "⚙️ Applying RuntimeClasses and Networking..."
kubectl apply -f infrastructure/k8s/runtime-class.yaml
kubectl apply -f infrastructure/k8s/service.yaml

# 5. DEPLOYING LOBES
echo "🛸 Launching the Swarm..."

# Define full image paths
REPO_PATH="us-central1-docker.pkg.dev/$PROJECT_ID/smos-repo"
AGENT_IMAGE="$REPO_PATH/smos-agent:latest"
DISPATCHER_IMAGE="$REPO_PATH/smos-dispatcher:latest"

# Update deployments with the correct images before applying
# (Using sed to swap placeholders if necessary, or assuming yaml points to these tags)
kubectl set image deployment/smos-agents-deployment smos-agent=$AGENT_IMAGE --local -o yaml | kubectl apply -f -
kubectl set image deployment/smos-golden-agent golden-agent=$AGENT_IMAGE --local -o yaml | kubectl apply -f -

# 5.1 Golden Agent (The Template)
kubectl apply -f infrastructure/k8s/snapshot-deployment.yaml


# 5.2 Main Agent Swarm
kubectl apply -f infrastructure/k8s/deployment.yaml

# 6. VERIFICATION
echo "🛰️ Waiting for Golden Agent to be Ready for Snapshotting..."
kubectl wait --for=condition=ready pod -l app=smos-golden --timeout=300s

echo "🚀 DEPLOYMENT COMPLETE"
echo "Check logs: kubectl logs -l app=smos"
echo "Run Diagnostic: PYTHONPATH=. ./.venv/bin/python scripts/setup_check.py"
