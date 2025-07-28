#!/bin/bash

# === Titre visuel dans le terminal
echo "🚀 LANCEMENT IA DOC SEARCH"

# === Activation de l'environnement virtuel
if [ -d "venv" ]; then
    echo "📦 Activation de l'environnement virtuel..."
    source venv/bin/activate
else
    echo "❌ Le dossier 'venv/' est introuvable. Créez-le avec : python3 -m venv venv"
    exit 1
fi

# === Lancer Streamlit (frontend)
echo "🖥️ Lancement de Streamlit..."
streamlit run frontend.py &

# === Lancer le Watcher
echo "👁️ Lancement du Watcher (fichiers)..."
python automation/watcher.py &

# === Ouvrir le navigateur
echo "🌐 Ouverture de l'interface sur http://localhost:8501"
open http://localhost:8501

# === Attendre que les deux processus se terminent (garde le terminal ouvert)
wait
