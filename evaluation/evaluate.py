import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# Ajout du path racine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 📥 Imports internes
from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks, search_index
from sentence_transformers import SentenceTransformer


# === Métrique de précision@k ===
def precision_at_k(pred_chunks, expected_keywords):
    hits = 0
    for chunk in pred_chunks:
        if any(keyword.lower() in chunk.lower() for keyword in expected_keywords):
            hits += 1
    return hits / len(pred_chunks)


# === Évaluation Precision@k ===
def evaluate_precision_at_k(doc_path, query_path, top_k=3, export_csv="evaluation/scores/precision_at_3.csv"):
    print("[INFO] Début évaluation Precision@k")

    text = extract_text(doc_path)
    cleaned = clean_text(text)
    chunks = split_text_spacy(cleaned)
    embeddings = generate_embeddings(chunks)

    index = create_faiss_index(embeddings.shape[1])
    index_chunks(index, embeddings)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open(query_path, encoding="utf-8") as f:
        queries = json.load(f)

    results = []
    for q in queries:
        question = q["question"]
        keywords = q["expected_keywords"]
        vec = model.encode([question], convert_to_numpy=True)
        ids, _ = search_index(index, vec, top_k=top_k)
        pred_chunks = [chunks[i] for i in ids]
        score = precision_at_k(pred_chunks, keywords)
        results.append({"question": question, "precision@3": round(score, 2)})

    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(export_csv), exist_ok=True)
    df.to_csv(export_csv, index=False)

    print(df)
    plt.figure(figsize=(10, 4))
    plt.barh(df["question"], df["precision@3"], color="skyblue")
    plt.xlabel("Precision@3")
    plt.title("Évaluation des requêtes (recherche sémantique)")
    plt.xlim(0, 1.05)
    plt.tight_layout()
    plt.show()


# === Évaluation BLEU / ROUGE ===
def evaluate_bleu_rouge(refs_path="evaluation/refs.json"):
    print("[INFO] Début évaluation BLEU/ROUGE")
    with open(refs_path, encoding="utf-8") as f:
        data = json.load(f)

    bleu_scores = []
    rouge_scores = []

    rouge = Rouge()

    for pair in data:
        ref = pair["reference"]
        gen = pair["generated"]

        # BLEU
        ref_tokens = ref.split()
        gen_tokens = gen.split()
        bleu = sentence_bleu([ref_tokens], gen_tokens, weights=(0.5, 0.5))
        bleu_scores.append({"BLEU": round(bleu, 3)})

        # ROUGE
        rouge_result = rouge.get_scores(gen, ref)[0]
        rouge_scores.append({
            "ROUGE-1": round(rouge_result["rouge-1"]["f"], 3),
            "ROUGE-2": round(rouge_result["rouge-2"]["f"], 3),
            "ROUGE-L": round(rouge_result["rouge-l"]["f"], 3)
        })

    # DataFrames et export
    df_bleu = pd.DataFrame(bleu_scores)
    df_rouge = pd.DataFrame(rouge_scores)

    df_bleu.to_csv("evaluation/scores/bleu_scores.csv", index=False)
    df_rouge.to_csv("evaluation/scores/rouge_scores.csv", index=False)

    print("[BLEU scores]")
    print(df_bleu)
    print("\n[ROUGE scores]")
    print(df_rouge)

    # Graphiques
    df_bleu.plot(kind="bar", title="BLEU scores", legend=False)
    plt.ylabel("Score BLEU")
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.show()

    df_rouge.plot(kind="bar", title="ROUGE scores")
    plt.ylabel("Score ROUGE")
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.show()


# === Lancer tout depuis __main__ ===
if __name__ == "__main__":
    evaluate_precision_at_k(
        doc_path="data/uploads/test_doc.pdf",
        query_path="evaluation/queries.json"
    )
    evaluate_bleu_rouge("evaluation/refs.json")



