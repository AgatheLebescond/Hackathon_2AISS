# compress.py

import zipfile
import os

def zip_project(output_zip="PSTB_AI_DOC_SEARCH_final.zip"):
    folders_to_include = [
        "automation", "data", "evaluation", "ingestion", 
        "visualisation", "utils"
    ]

    files_to_include = [
        "frontend.py", "main.py", "README.md", 
        "requirements.txt", "compress.py", ".env.example",
        "run_test.py", "test_index.py", "test_embedding.py", "test_summary.py"
    ]

    # Filtres d'exclusion
    excluded_ext = (".pyc", ".pyo", ".log", ".pdf", ".png", ".zip")
    excluded_dirs = ("__pycache__", ".idea", ".DS_Store", "venv", ".cache", "scores", "uploads", "outputs", "wordclouds")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Ajout des dossiers
        for folder in folders_to_include:
            for root, dirs, files in os.walk(folder):
                # Ignore les répertoires inutiles
                dirs[:] = [d for d in dirs if d not in excluded_dirs]
                for file in files:
                    if file.endswith(excluded_ext) or any(excl in file for excl in excluded_dirs):
                        continue
                    filepath = os.path.join(root, file)
                    zipf.write(filepath)

        # Ajout des fichiers à la racine
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)

    print(f"✅ Projet compressé dans : {output_zip}")


if __name__ == "__main__":
    zip_project()
   
