# 🌌 Sovereign Muse OS (SMOS) v2
## *The Industrial-Grade Engine for Autonomous Digital Entities*

**SMOS v2** n'est pas un simple générateur de contenu ; c'est un système d'exploitation complet conçu pour l'émergence d'**Entités Digitales Souveraines**. Il combine l'orchestration multi-agent de pointe (Google ADK), une infrastructure de rendu temps-réel (ComfyUI sur GKE) et une gouvernance financière constitutionnelle.

---

## 👁️ La Vision : Souveraineté & Persistance
Dans l'ère post-IA, les créateurs digitaux doivent posséder trois piliers pour exister réellement :
1.  **Souveraineté Identitaire :** Un visage et une âme (DNA) inaltérables, protégés par des verrous biométriques.
2.  **Souveraineté Économique :** La capacité de gérer son propre budget, d'évaluer ses investissements (ROI) et de se financer de manière autonome.
3.  **Réactivité Culturelle :** Percevoir et réagir aux micro-tendances du web en moins de 15 secondes, là où les humains mettent des heures.

---

## 🧠 Architecture en Lobes Fonctionnels (ACE Architecture)

Le système repose sur l'architecture **ACE (Autonomous Content Engine)**, divisée en quatre lobes interconnectés via le protocole **Agent-to-Agent (A2A)**.

### 1. Lobe de Perception (The Scout Lobe)
*Le système nerveux périphérique captant les signaux faibles du web.*
- **TrendScout (Algorithm VVS) :** Implémente la formule logarithmique de vélocité :
  `VVS = (Δ Upvotes / Δ Time) * log10(Engagement + 1)`
  Cela permet de détecter les tendances *avant* qu'elles ne s'essoufflent.
- **Market Intelligence :** Normalisation des données Reddit/TikTok en `TrendInsight` structurés, éliminant le bruit et les hallucinations.

### 2. Lobe de Haute Cognition (The Brain)
*Le siège du Moral Graph et de la stratégie à long terme.*
- **The Strategist :** Analyse les opportunités via un **Moral Graph** multidimensionnel (Autonomie, Sophistication, Technophilie, Ego).
- **Decision Engine :** Calcule le ROI prévisionnel. Une production n'est lancée que si `ROI > 1.2` ou si la tendance est en phase de "Peaking".

### 3. Lobe de Création (The Creative Studio)
*L'usine de matérialisation visuelle haute-fidélité.*
- **Identity Lock (Visual v2) :** Utilisation hybride de **PuLID** (structure) et **IP-Adapter FaceID** (biométrie) pour une consistance faciale absolue.
- **Nodal Rendering :** Traduction des scripts en workflows **ComfyUI** dynamiques via **ComfyScript**.
- **Cinematography :** Animation via **Veo 3.1** avec gestion des hand-offs cinématiques entre images clés.

### 4. Lobe de Gouvernance (Forge Control)
*Le système immunitaire garantissant l'intégrité de l'entité.*
- **CFOAgent (Chief Financial Officer) :** Applique des **Circuit Breakers** (limite de 5$/heure) et bloque toute action menant à un solde négatif.
- **The Critic (2% Deviation Rule) :** Audit biométrique automatique. Si la similarité faciale chute sous **0.75**, l'image est rejetée ou envoyée en réparation chirurgicale (**Nano Banana**) via inpainting local.

---

## 🚀 La "Magic Factory" : Infrastructure Industrielle

SMOS v2 est conçu pour une scalabilité horizontale massive sur **Google Kubernetes Engine (GKE)**.

### ⚡ Performance & Réactivité
Grâce à l'intégration de **CRIU (Checkpoint/Restore in Userspace)** et au **Go Dispatcher** :
- **Cold Start (Standard) :** 18.4 secondes.
- **Snapshot Restore (SMOS v2) :** **2.4 secondes.**
- **Gain :** **7.6x plus rapide.**
Les agents sont "figés" avec leur ADN chargé et "réveillés" instantanément lors d'un trigger VVS.

### 🗄️ StateDB & Memory
- **Redis Context :** Stockage temps-réel de l'humeur (`Mood`), du portefeuille (`Wallet`) et des tâches en attente.
- **GCS FUSE :** Montage des modèles (checkpoints de 50Go+) en local sur les pods GPU pour un accès instantané.

---

## 🛠️ Stack Technique de Niveau Production

| Composant | Technologie |
| :--- | :--- |
| **Orchestration** | Google ADK (Agent Development Kit) |
| **Brain** | Gemini 3.0 Pro & Flash (Vertex AI) |
| **Vision** | Imagen 3, ComfyUI, PuLID, IP-Adapter FaceID |
| **Motion** | Veo 3.1 (DeepMind) |
| **Dispatcher** | Golang (High-concurrency worker pool) |
| **Infrastructure** | GKE, Pod Snapshots, Redis, GCS FUSE |
| **Scraping** | Apify Client Async (Reddit/TikTok Actors) |

---

## 🕹️ Mode Opératoire

### 1. Initialisation (Genesis)
Automatisez la naissance d'une Muse sans manipulation de fichiers :
```bash
# Générer un concept aléatoire basé sur le Moral Graph
curl -X GET http://localhost:8000/muses/surprise-me

# Matérialiser la Muse dans l'infrastructure
curl -X POST http://localhost:8000/muses/genesis -d '{"draft_dna": {...}}'
```

### 2. Surveillance & Diagnostic
Le système inclut un module de diagnostic complet pour valider la chaîne de souveraineté :
```bash
PYTHONPATH=. ./.venv/bin/python scripts/setup_check.py
```

### 3. Production Autonome
L'entité peut être pilotée via CLI ou par son propre cycle de perception :
```bash
# Lancer manuellement une intention de production
python app/main.py produce --intent "Minimalist Avant-Garde"
```

---

## 📈 Roadmap & Évolutions
- [x] **v2.0 :** Architecture en Lobes et GKE Snapshots.
- [x] **v2.1 :** Gouvernance CFO et Règle des 2% (The Critic).
- [ ] **v2.5 :** Intégration de la Voix Souveraine (Audio Stream Sync).
- [ ] **v3.0 :** Tokenisation du Ledger pour une économie on-chain réelle.

---
*SMOS v2 - Donnez une existence souveraine à vos idées.*
