import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings

# === Charger un fichier à tester ===
file_path = os.path.join("data", "uploads", "test_doc.pdf")

# === Pipeline : texte → chunks → vecteurs ===
print("📥 Extraction...")
text = extract_text(file_path)

print("🧹 Nettoyage...")
cleaned = clean_text(text)

print("✂️ Découpage...")
chunks = split_text_spacy(cleaned, max_tokens=300)

print("🔢 Génération des vecteurs...")
embeddings = generate_embeddings(chunks)

print(f"✅ {len(embeddings)} vecteurs générés. Dimensions : {embeddings.shape[1]}")
