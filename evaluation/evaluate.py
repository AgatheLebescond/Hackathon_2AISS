import os
import sys

# 🔧 Ajoute la racine du projet au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 Ajouter racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks, search_index
from sentence_transformers import SentenceTransformer

# === Charger requêtes test ===
with open("evaluation/queries.json", encoding="utf-8") as f:
    queries = json.load(f)

# === Charger document
file_path = os.path.join("data", "uploads", "test_doc.pdf")
text = extract_text(file_path)
cleaned = clean_text(text)
chunks = split_text_spacy(cleaned)
embeddings = generate_embeddings(chunks)

# === Index FAISS
index = create_faiss_index(embeddings.shape[1])
index_chunks(index, embeddings)

model = SentenceTransformer("all-MiniLM-L6-v2")

# === Fonction de métrique
def precision_at_k(pred_chunks, expected_keywords):
    hits = 0
    for chunk in pred_chunks:
        if any(keyword.lower() in chunk.lower() for keyword in expected_keywords):
            hits += 1
    return hits / len(pred_chunks)

# === Évaluation
results = []
for q in queries:
    question = q["question"]
    keywords = q["expected_keywords"]
    vec = model.encode([question], convert_to_numpy=True)
    ids, _ = search_index(index, vec, top_k=3)
    pred_chunks = [chunks[i] for i in ids]
    score = precision_at_k(pred_chunks, keywords)

    results.append({"question": question, "precision@3": round(score, 2)})

# === Affichage tabulaire
df = pd.DataFrame(results)
print(df)

# === Affichage graphique
plt.figure(figsize=(10, 4))
plt.barh(df["question"], df["precision@3"], color="skyblue")
plt.xlabel("Precision@3")
plt.title("Évaluation des requêtes")
plt.xlim(0, 1.05)
plt.tight_layout()
plt.show()

