`README.md`,
## 🎓 Contexte

Ce projet a été développé dans le cadre du **Hackathon 2 — Team Invader**, dans une formation avancée en **intelligence artificielle générative**.

Il combine les technologies de **recherche sémantique**, de **résumé automatique**, d’**analyse de sentiment**, et d’**extraction d’articles web** pour fournir une application complète, 100% locale, de lecture assistée par IA.

---

## 🎯 Objectifs

| Objectif                                                            | Compétence associée                                |
| ------------------------------------------------------------------- | -------------------------------------------------- |
| Extraction automatique de texte (PDF, DOCX, articles en ligne)      | Parsing multi-format / HTML / API                  |
| Nettoyage et découpage NLP                                          | spaCy, segmentation linguistique                   |
| Embedding vectoriel                                                 | `sentence-transformers`, MiniLM                    |
| Recherche vectorielle                                               | FAISS, Similarité Cosine                           |
| Résumé génératif                                                    | Modèle `DistilBART` pré-entraîné                   |
| Question-réponse contextuelle                                       | Vectorisation + top-k context chunks               |
| Analyse de sentiment                                                | TextBlob / Transformers (multilingual BERT)        |
| Nuage de mots                                                       | WordCloud, Matplotlib                              |
| Évaluation des résumés                                              | BLEU, ROUGE, Precision@3                           |
| Interface interactive                                               | Streamlit                                          |

---

## ⚙️ Fonctionnalités principales

- 📄 Upload de documents PDF ou DOCX
- 🌐 URL d’article (via NewsAPI ou requête directe)
- ❓ Questions libres en langage naturel
- 🔎 Résultats contextuels pertinents (vector search)
- 📝 Résumé généré automatiquement (génératif)
- 📊 Analyse de sentiment globale
- ☁️ Visualisation du vocabulaire dominant (nuage de mots)
- 📥 Export (.txt, .pdf, .png)
- 📈 Évaluation via BLEU / ROUGE

---

## 🧱 Pipeline IA

```text
1. Upload fichier / saisie URL
2. Extraction texte brut
3. Nettoyage + découpage
4. Vectorisation par blocs
5. Indexation FAISS
6. Recherche vectorielle (top-k)
7. Résumé généré (DistilBART)
8. Analyse de sentiment
9. Nuage de mots
10. Affichage / export
🖥️ Interface utilisateur (Streamlit)

📁 Téléversement de fichier local
🌍 Extraction d’articles web via URL
❓ Moteur de recherche contextuel
📝 Résumé synthétique
📊 Score de sentiment (positif/neutre/négatif)
☁️ Nuage de mots dynamique
📤 Boutons de téléchargement (résumé, log, visuel)
📁 Arborescence du projet


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
│   └── scores/
│       ├── bleu_scores.csv
│       ├── rouge_scores.csv
├── visualisation/
│   └── wordclouds/
├── frontend.py
├── compress.py
├── requirements.txt
└── README.md

✅ Résultats obtenus

🔁 Traitement automatisé de documents et d’articles en ligne
🧠 Résumé cohérent en langage naturel
🔍 Recherche sémantique top-k
📊 Analyse de tonalité (score + mots dominants)
☁️ Nuage de mots cliquable
📈 Évaluation BLEU / ROUGE intégrée
📦 Projet packagé, prêt à être déployé en local
---

