# 🧠 Moteur de Recherche, Résumé Automatique et Analyse d'Articles avec IA Générative

---

## 🎓 Contexte pédagogique

Ce projet a été réalisé dans le cadre du **Hackathon 2 — Team Invader**, au sein d'une formation bootcamp.

Il combine les technologies de **recherche sémantique**, de **résumé automatique**, et d’**extraction d’articles web** pour fournir une application complète, 100% locale.Nous avons pris comme exemple la petition contre l'abrogation de la loi Duplomb.

---

## 🌟 Objectifs pédagogiques

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
               |
| Interface interactive                       | Streamlit                                |

---

## ⚙️ Fonctionnalités principales

- 📄 Upload de documents PDF ou DOCX
- 🌐 Extraction automatique d’articles via URL
- 🔗 **Connexion à NewsAPI pour télécharger le contenu complet d’un article à partir de son URL**
- 🖼️ **Récupération automatique des métadonnées de l’article** : titre, auteur, date de publication, **URL de l’image d’en-tête**, nom du journal
- ❓ Questions en langage naturel (question answering vectoriel)
- 🔍 Recherche vectorielle top-k contextuelle (passages les plus pertinents)
- 📝 Résumé généré automatiquement via modèle Transformer
- 🧽 Résumé guidé par **prompt thématique** : climat, mobilisation citoyenne, loi Duplomb
- 📤 Export des résultats : `.txt`, `.pdf`, `.png`
---

## 🔁 Pipeline IA complet

```text
1. Upload d’un fichier PDF/DOCX ou saisie d’une URL
2. Extraction du texte (pdfplumber / NewsAPI / HTML parser)
3. Extraction des métadonnées : titre, date, image, journal (si disponible)
4. Nettoyage et découpage (spaCy)
5. Vectorisation sémantique (MiniLM)
6. Indexation locale via FAISS
7. Saisie d’une question libre → recherche contextuelle top-k
8. Choix entre deux boutons :
   - 📄 Résumé classique (neutre)
   - 🌍 Résumé thématique (mobilisation citoyenne, climat, loi Duplomb)
9. Affichage dynamique via Streamlit (texte + métadonnées + image + nuage)
10. Export des résultats : `.txt`, `.pdf`, `.png`
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


La clé est ensuite chargée dans le code via :

```python
import os
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
```

Le système récupère automatiquement les **métadonnées** suivantes pour chaque article extrait :

- 🕒 Date et heure de publication
- 🖼️ Image d’en-tête (URL)
- ✍️ Auteur, nom du **journal ou magazine** (source), si disponibles

---

## 🖥️ Interface utilisateur (Streamlit)

- 📁 Téléversement de fichiers PDF/DOCX
- 🌍 Collage d’une **URL d’article d’actualité** (via NewsAPI)
- 🕒 Affichage de la **date de publication** de l’article
- 🖼️ Affichage de l’**image d’illustration** (si présente)
- 📰 Affichage du **nom du journal ou média**
- ❓ Saisie d’une question libre
- 🔍 Recherche sémantique des passages pertinents
- 📝 Deux types de résumés générés :
  - 📄 Résumé classique (neutre)
  - 🌍 Résumé thématique (mobilisation citoyenne, climat, loi Duplomb)
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
├── visualisation/
│   └── wordclouds/
├── frontend.py
├── compress.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ✅ Résultats obtenus

- 🔁 Traitement automatisé de fichiers et d’articles web
- 🧠 Résumés générés localement en deux modes : classique ou thématique
- 🔍 Recherche sémantique top-k des réponses contextuelles
- 📦 Projet packagé, prêt à être exécuté localement

