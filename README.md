# PSTB_ai_doc_search – Pipeline IA pour la veille documentaire et l’analyse sémantique

Ce projet a été réalisé dans le cadre de l’**exercice 3 du hackathon final du bootcamp IA & Data 2025**. Il vise à automatiser la veille citoyenne sur la pétition demandant l’abrogation de la loi Duplomb, à travers un pipeline de traitement de documents, résumé automatique, recherche sémantique et visualisation interactive.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Objectifs du projet

- 📥 Extraire des articles via NewsAPI ou PDF
- 🧽 Nettoyer les textes pour NLP
- 🧠 Résumer automatiquement les documents
- 🔎 Rechercher de manière sémantique dans les contenus vectorisés
- 🧪 Évaluer les résumés (ROUGE / BLEU)
- 🖼️ Visualiser et interagir via une interface Streamlit

---

## 📁 Arborescence du projet

```
PSTB_ai_doc_search/
├── automation/
│   └── watcher.py
├── data/
│   ├── uploads/
│   └── outputs/
├── ingestion/
│   ├── extractor.py
│   ├── newsapi_fetcher.py
│   ├── article_to_pdf.py
│   ├── cleaner.py
│   └── processing/
│       ├── splitter.py
│       ├── embedder.py
│       ├── indexer.py
│       ├── summarizer.py
│       └── query_article.py
├── evaluation/
│   ├── evaluate.py
│   ├── bleu_rouge.py
│   ├── queries.json
│   └── scores/
│       ├── bleu_scores.csv
│       └── rouge_scores.csv
├── frontend.py
├── compress.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/ton-utilisateur/PSTB_ai_doc_search.git
cd PSTB_ai_doc_search
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 🚀 Utilisation

```bash
python ingestion/newsapi_fetcher.py
python ingestion/cleaner.py
python ingestion/processing/summarizer.py
python ingestion/processing/embedder.py
python ingestion/processing/indexer.py
python ingestion/processing/query_article.py
streamlit run frontend.py
```

---

## 🧪 Évaluation

```bash
python evaluation/evaluate.py
```

Résultats enregistrés dans `evaluation/scores/`.

---

## 🔐 Exemple `.env`

```env
NEWSAPI_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_key
EMBEDDING_MODEL=text-embedding-ada-002
```

---

## 🧠 Technologies

- Python 3.10
- Streamlit
- spaCy, transformers
- scikit-learn
- OpenAI API
- NewsAPI

---

## 🙌 Auteur

Projet réalisé dans le cadre de l’**exercice 3 du hackathon du bootcamp IA & Data 2025**, appliqué à une veille citoyenne sur la pétition visant l’abrogation de la loi Duplomb.

Auteur·e : Agathe Le Bescond et Olivier de Cibeins
