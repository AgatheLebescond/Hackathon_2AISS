import os
import sys
import tempfile

import streamlit as st

# Assure les imports de modules internes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingestion.extractor import extract_text
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text_spacy
from ingestion.processing.embedder import generate_embeddings
from ingestion.processing.indexer import create_faiss_index, index_chunks, search_index
from ingestion.processing.summarizer import summarize_text
from sentence_transformers import SentenceTransformer

from ingestion.processing.export import export_summary_txt, export_summary_pdf


# === Initialisation globale ===
st.set_page_config(page_title="Recherche IA + Résumé", layout="wide")
st.title("🔎 Recherche intelligente dans vos documents")

if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = []
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None

model = SentenceTransformer("all-MiniLM-L6-v2")

# === Upload de document ===
uploaded_file = st.file_uploader("📤 Téléversez un document PDF ou DOCX", type=["pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("✅ Fichier chargé.")
    st.subheader("📥 Traitement du document...")

    raw_text = extract_text(tmp_path)
    cleaned = clean_text(raw_text)
    chunks = split_text_spacy(cleaned)

    st.session_state.doc_chunks = chunks
    embeddings = generate_embeddings(chunks)
    st.session_state.embeddings = embeddings

    faiss_index = create_faiss_index(embeddings.shape[1])
    index_chunks(faiss_index, embeddings)
    st.session_state.faiss_index = faiss_index

    st.success(f"✅ {len(chunks)} blocs indexés.")
    os.remove(tmp_path)

# === Interface de recherche ===
if st.session_state.faiss_index:
    st.subheader("❓ Posez une question sur le document")

    user_query = st.text_input("Votre question :", placeholder="Ex : Quels sont les types de comportement d’achat ?")

    if user_query:
        query_vec = model.encode([user_query], convert_to_numpy=True)
        indices, _ = search_index(st.session_state.faiss_index, query_vec, top_k=3)

        selected_chunks = [st.session_state.doc_chunks[i] for i in indices]

        st.divider()
        st.markdown("### 🧠 Blocs les plus pertinents :")
        for i, chunk in enumerate(selected_chunks):
            with st.expander(f"Chunk {i+1}"):
                st.write(chunk)

        full_text = " ".join(selected_chunks)
        summary = summarize_text(full_text)

        st.markdown("### 📝 Résumé généré :")
        st.success(summary)
        
        import tempfile
from ingestion.processing.export import export_summary_txt, export_summary_pdf

# === Export boutons
if st.button("💾 Télécharger le résumé"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as txt_file:
        export_summary_txt(summary, txt_file.name)
        st.download_button("⬇️ Télécharger .txt", data=open(txt_file.name, "rb"), file_name="resume.txt")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        export_summary_pdf(summary, pdf_file.name)
        st.download_button("⬇️ Télécharger .pdf", data=open(pdf_file.name, "rb"), file_name="resume.pdf")

st.sidebar.markdown("🧾 **Logs d’indexation**")

if st.sidebar.button("📖 Voir log.txt"):
    log_path = os.path.join("data", "outputs", "log.txt")
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as log_file:
            logs = log_file.read()
        st.sidebar.text_area("🗂 Journal des traitements :", logs, height=300)
    else:
        st.sidebar.warning("Aucun log détecté.")

