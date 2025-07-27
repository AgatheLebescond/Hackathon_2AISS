`README.md`, **projet Hackatho 2 Team BLUE de formation en IA générative**

Elle inclut :

* le contexte pédagogique et technique,
* les objectifs détaillés,
* les composants du pipeline avec justification des choix,
* la démarche de développement,
* l’évaluation chiffrée,
* les résultats concrets,
* la structure complète du projet.

---

## 🧠 `README.md` — Projet : Moteur de Recherche et Résumé Automatique de Documents avec IA Générative

---

### 🎓 Contexte

Ce projet a été réalisé dans le cadre d’une **formation avancée en intelligence artificielle générative**.
Il vise à appliquer les connaissances acquises en **traitement automatique du langage (NLP)**, en **modèles de langage pré-entraînés**, en **recherche vectorielle**, et en **développement d’interfaces intelligentes**.

---

## 🎯 Objectifs pédagogiques

| Objectif                                                       | Compétence associée                           |
| -------------------------------------------------------------- | --------------------------------------------- |
| Extraire automatiquement le texte de documents PDF et DOCX     | Extraction, parsing, gestion de formats       |
| Nettoyer et découper efficacement un corpus textuel            | NLP bas niveau (tokenisation, segmentation)   |
| Transformer le texte en vecteurs sémantiques                   | Sentence Embeddings, encodage dense           |
| Implémenter un moteur de recherche vectorielle local           | Indexation FAISS, similarité cosine           |
| Appliquer un modèle de résumé pré-entraîné de type Transformer | IA générative, résumé extractif/abstractive   |
| Créer une interface interactive simple à utiliser              | Streamlit, frontend rapide                    |
| Automatiser l’analyse de fichiers entrants                     | Programmation orientée événements (watchdog)  |
| Évaluer la pertinence des réponses générées                    | Métriques de précision, évaluation supervisée |

---

## 🧱 Description du système

L’objectif est de permettre à un utilisateur de :

1. **Téléverser un fichier** (PDF ou DOCX),
2. **Poser une question libre** en langage naturel,
3. Obtenir les **passages du texte les plus pertinents**,
4. Lire un **résumé synthétique généré automatiquement**.

Le tout en local, **sans cloud**, via un pipeline IA complet.

---

## ⚙️ Technologies et composants

| Composant      | Détail technique                                           | Pourquoi ce choix ?                                      |
| -------------- | ---------------------------------------------------------- | -------------------------------------------------------- |
| **Extraction** | `pdfplumber`, `docx2txt`                                   | Robuste pour formats texte courants                      |
| **Nettoyage**  | Normalisation basique (espaces, caractères spéciaux)       | Suffisant pour usage en français                         |
| **Découpage**  | `spaCy` avec `en_core_web_sm`                              | Reconnaissance grammaticale, découpage logique           |
| **Embeddings** | `all-MiniLM-L6-v2` (`sentence-transformers`)               | Léger, rapide, très bon pour similarité sémantique       |
| **Indexation** | `FAISS` (IndexFlatL2)                                      | Recherche vectorielle locale, performante et rapide      |
| **Recherche**  | Comparaison cosine entre question et vecteurs              | Recherche dense par similarité                           |
| **Résumé IA**  | `sshleifer/distilbart-cnn-12-6` (HuggingFace Transformers) | Résumé génératif pré-entraîné, fluide et pertinent       |
| **Interface**  | `Streamlit`                                                | Simplicité d’usage, affichage dynamique                  |
| **Automation** | `watchdog` + `winsound`                                    | Détection automatique + notification utilisateur Windows |
| **Évaluation** | `evaluate.py` avec `precision@3`, `matplotlib`, `pandas`   | Mesure objective de la qualité des réponses              |

---

## 🚀 Fonctionnement global

### 🔁 Pipeline automatisé :

```
1. Upload document (PDF / DOCX)
2. Extraction du texte brut
3. Nettoyage (suppression bruit)
4. Découpage en blocs cohérents (phrases, paragraphes)
5. Embeddings vectoriels de chaque bloc
6. Construction d’un index FAISS
7. Saisie de la question utilisateur
8. Recherche vectorielle (top-k chunks)
9. Résumé automatique des résultats (DistilBART)
10. Affichage + Export (résumé .txt, log .txt)
```

### 🧠 Objectif :

**Raccourcir le temps d’accès à l’information contenue dans un document long**, en combinant IA générative, vectorisation, et résumé automatique.

---

## 🖥️ Interface utilisateur (Streamlit)

Fonctionnalités disponibles :

* 📁 Téléversement de fichier PDF ou DOCX
* ❓ Saisie de question libre
* 🔍 Résultats affichés (chunks pertinents)
* 📝 Résumé généré automatiquement
* 💾 Boutons de téléchargement (.txt, .pdf)
* 📄 Visualisation du `log.txt` via la barre latérale

---

## 📁 Automatisation complète via `watcher.py`

### Fonctionnement :

* Surveille `data/uploads/`
* Dès qu’un fichier est ajouté :

  * Traitement complet
  * Résumé généré automatiquement
  * Résumé sauvegardé dans `data/outputs/`
  * Entrée dans `log.txt`
  * Notification sonore (Windows)

---

## 🧪 Évaluation des performances

📄 Fichier : `evaluation/evaluate.py`

Métrique utilisée : **Precision\@3**
(nom du ratio de réponses pertinentes dans les 3 meilleurs résultats FAISS)

### 🔍 Exemple de `queries.json` :

```json
[
  {
    "question": "quels sont les types de comportement d'achat ?",
    "expected_keywords": ["routinier", "complexe", "impulsif", "dissonance"]
  },
  {
    "question": "qu'est-ce que l'achat impulsif ?",
    "expected_keywords": ["émotion", "soudaine", "non planifié"]
  }
]
```

### 📊 Résultats obtenus :

| Question                       | Precision\@3 |
| ------------------------------ | ------------ |
| Types de comportements d’achat | `1.00` ✅     |
| Achat impulsif                 | `0.33` ⚠️    |
| Fidélisation client            | `0.66` ✔️    |

### 📁 Export :

* Fichier CSV : `evaluation/summary_results.csv`
* Graphique PNG : `evaluation/precision_chart.png`

---

## 📦 Packaging final

Utiliser `compress.py` pour générer une archive du projet complète :

```bash
python compress.py
```

📁 Génére : `PSTB_AI_DOC_SEARCH_final.zip`

---

## 🧭 Arborescence du projet

```
PSTB_ai_doc_search/
├── automation/              ← Watcher auto
├── data/
│   ├── uploads/             ← Fichiers à traiter
│   └── outputs/             ← Résumés générés, log
├── ingestion/
│   ├── extractor.py         ← Extraction PDF/DOCX
│   ├── cleaner.py           ← Nettoyage texte
│   └── processing/
│       ├── splitter.py      ← spaCy découpage
│       ├── embedder.py      ← Sentence Embeddings
│       ├── indexer.py       ← FAISS
│       ├── summarizer.py    ← Résumé IA
│       └── export.py        ← Export `.txt`, `.pdf`
├── evaluation/
│   ├── evaluate.py          ← Script test
│   ├── queries.json         ← Questions test
├── frontend.py              ← Interface utilisateur
├── compress.py              ← Script .zip
├── requirements.txt         ← Dépendances
└── README.md                ← Ce fichier
```

---

## ✅ Résultats du projet

* 🔧 Fonctionnement **entièrement automatisé**
* 🧠 Résumé cohérent généré localement
* 🔍 Recherche sémantique pertinente
* 📊 Évaluation mesurable et exportable
* 💾 Résumé + log archivés
* 👤 Interface utilisable par des non-techniques
* 📦 Projet packagé et prêt à livrer

---
