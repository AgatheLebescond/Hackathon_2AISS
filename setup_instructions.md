
# 🚀 Instructions d'installation et de démarrage du projet

## 📦 Pré-requis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Environnement virtuel recommandé (`venv` ou `conda`)

---

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-utilisateur/PSTB_ai_doc_search.git
cd PSTB_ai_doc_search

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# .\venv\Scripts\activate  # Sur Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## 🔐 Configuration

Créer un fichier `.env` à partir de l’exemple :

```bash
cp .env.example .env
```

Puis coller votre clé API personnelle NewsAPI :

```
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ Lancement de l’interface

```bash
streamlit run frontend.py
```

---

## 🔁 Lancement du traitement automatique (surveillance de dossier)

```bash
python automation/watcher.py
```

---

## 🧪 Évaluation automatique (BLEU / ROUGE / Precision@3)

```bash
python evaluation/evaluate.py
```

---

## 📤 Compression du projet pour livraison

```bash
python compress.py
```
