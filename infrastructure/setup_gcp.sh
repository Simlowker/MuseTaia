#!/bin/bash

# SMOS v2 - GCP Setup Script
# Description: Enables necessary Google Cloud APIs for the project.
# Usage: ./setup_gcp.sh

echo "🚀 Starting GCP Setup for SMOS v2..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: 'gcloud' command not found."
    echo "👉 Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    echo "OR run the following commands in the Google Cloud Shell (https://shell.cloud.google.com)"
    exit 1
fi

echo "✅ gcloud found. Enabling APIs..."

# Enable required services
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
    || { echo "❌ Failed to enable APIs"; exit 1; }

echo "✅ All APIs enabled successfully."
echo "👉 Next step: Configure your Quotas in the GCP Console using 'deployment_guide.md'."
