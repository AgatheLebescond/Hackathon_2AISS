import faiss
import numpy as np

def create_faiss_index(embedding_dim):
    """
    Crée un index FAISS L2 brut (IndexFlatL2) avec la dimension donnée.
    """
    return faiss.IndexFlatL2(embedding_dim)

def index_chunks(faiss_index, embeddings):
    """
    Ajoute les embeddings à l’index FAISS.
    """
    faiss_index.add(embeddings)

def search_index(faiss_index, query_vector, top_k=3):
    """
    Effectue une recherche dans l’index FAISS avec un vecteur de requête.
    Retourne les indices et les distances.
    """
    distances, indices = faiss_index.search(query_vector, top_k)
    return indices[0], distances[0]
