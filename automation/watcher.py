import os
import time
import sys
import winsound  # 🔔 notification sonore
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === Ajouter la racine du projet au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# === Imports internes
from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks
from ingestion.processing.summarizer import summarize_text
from ingestion.processing.export import export_summary_txt  # ← assure-toi que ce fichier existe

# === Répertoires
WATCH_DIR = "data/uploads/"
OUTPUT_DIR = "data/outputs/"

# === Création des dossiers si absents
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith((".pdf", ".docx")):
            return

        print(f"\n📥 Nouveau fichier détecté : {event.src_path}")

        try:
            # === Traitement NLP
            text = extract_text(event.src_path)
            cleaned = clean_text(text)
            chunks = split_text_spacy(cleaned)
            embeddings = generate_embeddings(chunks)
            index = create_faiss_index(embeddings.shape[1])
            index_chunks(index, embeddings)

            # === Génération résumé
            summary = summarize_text(" ".join(chunks[:3]))

            # === Export résumé
            basename = os.path.basename(event.src_path).rsplit(".", 1)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{basename}_{timestamp}_resume.txt"
            output_path = os.path.join(OUTPUT_DIR, output_file)
            export_summary_txt(summary, output_path)
            print(f"📝 Résumé exporté : {output_file}")

            # === Écriture log
            log_path = os.path.join(OUTPUT_DIR, "log.txt")
            with open(log_path, "a", encoding="utf-8") as log:
                log.write(f"[{timestamp}] {basename} → {len(chunks)} chunks, résumé généré : {output_file}\n")

            # === Notification sonore
            winsound.MessageBeep()
            print(f"🔔 Traitement terminé pour : {basename}\n")

        except Exception as e:
            print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(UploadHandler(), path=WATCH_DIR, recursive=False)
    observer.start()
    print(f"👁️ Surveillance de {WATCH_DIR} activée...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


