import zipfile
import os

def zip_project(output_zip="PSTB_AI_DOC_SEARCH_final.zip"):
    folders_to_include = [
        "automation", "data", "evaluation", "ingestion", "search", "utils"
    ]
    files_to_include = [
        "frontend.py", "main.py", "README.md",
        "requirements.txt", "run_test.py",
        "test_index.py", "test_embedding.py", "test_summary.py",
        "compress.py"
    ]

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder in folders_to_include:
            for root, _, files in os.walk(folder):
                for file in files:
                    path = os.path.join(root, file)
                    zipf.write(path)
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)

    print(f"✅ Projet compressé dans : {output_zip}")

if __name__ == "__main__":
    zip_project()
