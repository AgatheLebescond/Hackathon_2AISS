# 🧠 Moteur de Recherche, Résumé Automatique et Analyse d'Articles avec IA Générative

---

## 🎓 Contexte pédagogique

Ce projet a été réalisé dans le cadre du **Hackathon 2 — Team Invader**, au sein d'une formation avancée en **intelligence artificielle générative**.

Il combine les technologies de **recherche sémantique**, de **résumé automatique**, d’**analyse de sentiment**, et d’**extraction d’articles web** pour fournir une application complète, 100% locale, de lecture assistée par IA.

---

## 🎯 Objectifs pédagogiques

| Objectif                                    | Compétence développée                    |
| ------------------------------------------- | ---------------------------------------- |
| Extraction de texte (PDF/DOCX/articles web) | Parsing multi-format, HTML, API          |
| Extraction des métadonnées (date, image)    | Parsing HTML, traitement JSON NewsAPI    |
| Nettoyage et découpage NLP                  | spaCy, segmentation linguistique         |
| Embedding vectoriel                         | Sentence-Transformers (MiniLM)           |
| Recherche vectorielle                       | FAISS + similarité cosine                |
| Résumé génératif                            | DistilBART pré-entraîné                  |
| Question-réponse contextuelle               | Vectorisation + top-k context chunks     |
| Résumé guidé via prompt thématique          | Prompt engineering (mobilisation/climat) |
| Analyse de sentiment                        | TextBlob / Transformers                  |
| Nuage de mots                               | WordCloud, Matplotlib                    |
| Évaluation automatique des résumés          | BLEU, ROUGE, Precision\@3                |
| Interface interactive                       | Streamlit                                |

---

## ⚙️ Fonctionnalités principales

- 📄 Upload de documents PDF ou DOCX
- 🌐 Extraction automatique d’articles via URL
- 🔗 **Connexion à NewsAPI pour télécharger le contenu complet d’un article à partir de son URL**
- 🖼️ **Récupération automatique des métadonnées de l’article** : titre, auteur, date de publication, **URL de l’image d’en-tête**
- ❓ Questions en langage naturel (question answering vectoriel)
- 🔍 Recherche vectorielle top-k contextuelle (passages les plus pertinents)
- 📝 Résumé généré automatiquement via modèle Transformer
- 🧭 Résumé guidé par **prompt thématique** : climat, mobilisation citoyenne, loi Duplomb
- 📊 Analyse de sentiment (polarité globale)
- ☁️ Génération dynamique d’un nuage de mots à partir du texte analysé
- 📤 Export des résultats : `.txt`, `.pdf`, `.png`
- 📈 Évaluation automatique avec BLEU et ROUGE

---

## 🔁 Pipeline IA complet

```text
1. Upload d’un fichier PDF/DOCX ou saisie d’une URL
2. Extraction du texte (pdfplumber / NewsAPI / HTML parser)
3. Extraction des métadonnées : titre, date, image (si disponible)
4. Nettoyage et découpage (spaCy)
5. Vectorisation sémantique (MiniLM)
6. Indexation locale via FAISS
7. Saisie d’une question libre → recherche contextuelle top-k
8. Résumé généré automatiquement (DistilBART)
   ↳ avec prompt : "Résume en insistant sur la mobilisation citoyenne, le climat et les critiques de la loi Duplomb"
9. Analyse de sentiment (TextBlob ou modèle BERT multilingue)
10. Génération d’un nuage de mots
11. Affichage dynamique via Streamlit (texte + métadonnées + image)
12. Export des résultats : `.txt`, `.pdf`, `.png`
```

---

## 🔐 Intégration de NewsAPI

Le projet intègre [**NewsAPI**](https://newsapi.org/) pour extraire le contenu d’articles d’actualité directement à partir d’une URL.

### ⚙️ Prérequis :

Un fichier `.env.example` est fourni pour aider à la configuration locale :

```env
# .env.example
NEWS_API_KEY=your_api_key_here
```

➡️ **À faire** :

- Copier `.env.example` → `.env`
- Remplacer `your_api_key_here` par votre vraie clé NewsAPI

1. Créer un compte gratuit sur [https://newsapi.org/](https://newsapi.org/)
2. Récupérer une clé d’API personnelle
3. La stocker dans un fichier `.env` (ou comme variable d’environnement) :

```
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ Ne jamais versionner cette clé sur GitHub

La clé est ensuite chargée dans le code via :

```python
import os
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
```

Le système récupère automatiquement les **métadonnées** suivantes pour chaque article extrait :

- 🕓 Date et heure de publication
- 🖼️ Image d’en-tête (URL)
- ✍️ Auteur, nom du **journal ou magazine** (source), si disponibles

---

## 🖥️ Interface utilisateur (Streamlit)

- 📁 Téléversement de fichiers PDF/DOCX
- 🌍 Collage d’une **URL d’article d’actualité** (via NewsAPI)
- 🕓 Affichage de la **date de publication** de l’article
- 🖼️ Affichage de l’**image d’illustration** (si présente)
- 📰 Affichage du **nom du journal ou média**
- ❓ Saisie d’une question libre
- 🔍 Recherche sémantique des passages pertinents
- 📝 Résumé automatique avec ou sans prompt thématique
- 📊 Score de sentiment (positif, neutre, négatif)
- ☁️ Nuage de mots généré dynamiquement
- 📥 Boutons d’export : résumé (.txt), visuel (.png), log

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
│       ├── query_article.py
│       ├── sentiment_analyzer.py
│       └── wordcloud_generator.py
├── evaluation/
│   ├── evaluate.py
│   ├── queries.json
│   ├── bleu_rouge.py
│   ├── references.json
│   └── scores/
│       ├── bleu_scores.csv
│       ├── rouge_scores.csv
├── visualisation/
│   └── wordclouds/
├── frontend.py
├── compress.py
├── requirements.txt
└── README.md
```

---

## ✅ Résultats obtenus

- 🔁 Traitement automatisé de documents et d’articles en ligne
- 🧠 Résumé génératif fluide et cohérent
- 🔍 Recherche sémantique localisée et pertinente
- 🎯 Résumés contextualisés via prompt (mobilisation, climat, loi Duplomb)
- 📊 Analyse de sentiment intégrée (avec score)
- ☁️ Nuage de mots généré à partir des passages clés
- 🕓 Affichage de la date de publication pour les articles
- 🖼️ Image d’en-tête visible dans l’interface
- 📤 Export des résultats en local : `.txt`, `.pdf`, `.png`
- 📈 Évaluation automatique intégrée (BLEU / ROUGE)
- 💻 Interface utilisable par des profils non techniques
- 📦 Projet packagé et prêt à être diffusé

