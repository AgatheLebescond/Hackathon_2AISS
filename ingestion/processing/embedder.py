from sentence_transformers import SentenceTransformer

# Chargement du modèle une seule fois
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks):
    """
    Reçoit une liste de strings (chunks) et retourne la liste des vecteurs d'embeddings.
    """
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    return embeddings
