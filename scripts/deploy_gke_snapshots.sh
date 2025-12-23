#!/bin/bash
# SMOS v2 : Déploiement Industriel avec Pod Snapshots

PROJECT_ID=$(gcloud config get-value project)
LOCATION="us-central1"
CLUSTER_NAME="smos-cpu-cluster"

echo "🚀 Lancement du déploiement SMOS v2..."

# 1. Appliquer les configurations Kubernetes
kubectl apply -f infrastructure/k8s/env-config.yaml

# 2. Déployer l'Agent de base (Le Golden Pod) et le Frontend
kubectl apply -f infrastructure/k8s/deployment.yaml

echo "⏳ Attente de l'initialisation du Golden Pod (DNA Loading)..."
kubectl wait --for=condition=ready pod -l app=smos-backend --timeout=120s

# 3. Déployer le Dispatcher Go (Gestionnaire du Burst Mode)
# Note: Nous utilisons le déploiement standard pour le Dispatcher, implémenté en Go.
# kubectl apply -f infrastructure/k8s/snapshot-deployment.yaml # À créer si besoin spécifique
kubectl apply -f infrastructure/k8s/deployment.yaml # Inclut déjà le dispatcher

# 4. Initialisation de la Matrix (Context Caching)
# echo "🧠 Initialisation du cache contextuel sur Vertex AI..."
# python3 -m app.matrix.context_cache --action init

echo "✅ Système prêt. Le Dispatcher Go surveille maintenant les tendances."
