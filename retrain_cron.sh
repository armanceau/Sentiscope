#!/bin/bash
# Script shell pour automatiser le réentraînement du modèle

# Se placer dans le bon répertoire (à adapter selon le déploiement)
cd "$(dirname "$0")"

# Charger l'environnement virtuel si présent
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Variables d'environnement éventuelles
# export DATABASE_URL="mysql+pymysql://root:root@localhost:3306/sentiscope"

echo "========================================"
echo "Début du réentraînement : $(date)"

# Lancer le script de modèle
python model.py --model-path models/sentiment_model.joblib

echo "Réentraînement terminé : $(date)"
echo "========================================"
