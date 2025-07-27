import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks, search_index
from ingestion.processing.summarizer import summarize_text
from sentence_transformers import SentenceTransformer

# === Pipeline complet jusqu'au résumé ===

# Chargement document
file_path = os.path.join("data", "uploads", "test_doc.pdf")
text = extract_text(file_path)
cleaned = clean_text(text)
chunks = split_text_spacy(cleaned)

# Embedding des chunks
embeddings = generate_embeddings(chunks)
index = create_faiss_index(embeddings.shape[1])
index_chunks(index, embeddings)

# Embedding de requête
query = "quels sont les types de comportement d'achat ?"
model = SentenceTransformer("all-MiniLM-L6-v2")
query_vector = model.encode([query], convert_to_numpy=True)

# Recherche
indices, _ = search_index(index, query_vector, top_k=3)
retrieved_chunks = [chunks[i] for i in indices]

# Concaténation + résumé
concatenated_text = " ".join(retrieved_chunks)
summary = summarize_text(concatenated_text)

print("\n📄 Résumé généré :\n")
print(summary)
