import os
import sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks, search_index
from sentence_transformers import SentenceTransformer

# === Chargement du fichier source ===
file_path = os.path.join("data", "uploads", "test_doc.pdf")
text = extract_text(file_path)
cleaned = clean_text(text)
chunks = split_text_spacy(cleaned, max_tokens=300)

# === Embedding des chunks ===
print("🔢 Génération des vecteurs...")
embeddings = generate_embeddings(chunks)

# === Création de l'index FAISS ===
dim = embeddings.shape[1]
index = create_faiss_index(dim)
index_chunks(index, embeddings)
print(f"✅ Index FAISS créé avec {len(chunks)} chunks.")

# === Simulation d'une requête ===
model = SentenceTransformer("all-MiniLM-L6-v2")
query = " loi Duplomb " "climat" 
query_vector = model.encode([query], convert_to_numpy=True)

# === Recherche FAISS ===
indices, distances = search_index(index, query_vector, top_k=3)

print("\n🔍 Résultats de recherche :\n")
for rank, idx in enumerate(indices):
    print(f"[{rank+1}] (distance {distances[rank]:.4f})\n{chunks[idx]}\n")
