import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy  # ✅ chemin correct


# === Chemin du fichier à tester ===
file_path = os.path.join("data", "uploads", "test_doc.pdf")  # ou test_doc.docx

# === Vérification fichier ===
if not os.path.isfile(file_path):
    print(f"❌ Fichier non trouvé : {file_path}")
    sys.exit(1)

# === Étape 1 : Extraction ===
print("📥 Extraction...")
try:
    raw_text = extract_text(file_path)
    print(f"✅ Texte brut extrait :\n{raw_text[:500]}...\n")
except Exception as e:
    print(f"❌ Erreur d'extraction : {e}")
    sys.exit(1)

# === Étape 2 : Nettoyage ===
print("🧹 Nettoyage...")
cleaned = clean_text(raw_text)
print(f"✅ Texte nettoyé :\n{cleaned[:500]}...\n")

# === Étape 3 : Découpage ===
print("✂️ Découpage...")
chunks = split_text_spacy(cleaned, max_tokens=300)
print(f"✅ {len(chunks)} chunks générés.\n")

for i, chunk in enumerate(chunks[:3]):  # Affiche les 3 premiers chunks
    print(f"--- Chunk {i+1} ---\n{chunk}\n")


