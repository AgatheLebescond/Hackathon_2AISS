# frontend.py

import os
import streamlit as st

from ingestion.extractor import extract_text_from_file
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text
from ingestion.processing.embedder import embed_chunks
from ingestion.processing.indexer import build_faiss_index
from ingestion.processing.summarizer import generate_summary, generate_thematic_summary
from ingestion.processing.sentiment_analyzer import analyze_sentiment
from ingestion.processing.wordcloud_generator import generate_wordcloud
from ingestion.newsapi_fetcher import fetch_article_from_url


# === Configuration Streamlit
st.set_page_config(page_title="AI Résumeur", layout="wide")
st.title("🧠 Résumeur intelligent d'articles & PDF")

# === Fonctions utilitaires ===

def save_uploaded_file(uploaded_file):
    """Sauvegarde un fichier uploadé dans data/uploads/"""
    filepath = os.path.join("data/uploads", uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    return filepath


def process_text_pipeline(raw_text):
    """Pipeline NLP complet : nettoyage, split, embedding, index"""
    cleaned = clean_text(raw_text)
    chunks = split_text(cleaned)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)
    return cleaned, chunks, index


def display_summary_section(chunks, thematic=False, theme=None):
    """Affichage d’un résumé généré automatiquement"""
    if thematic and theme:
        summary = generate_thematic_summary(chunks, theme=theme)
        st.subheader(f"🌍 Résumé thématique : {theme}")
    else:
        summary = generate_summary(chunks)
        st.subheader("📝 Résumé généré")
    st.success(summary)
    return summary


def display_analysis(summary, cleaned_text, doc_id):
    """Analyse de sentiment et nuage de mots"""
    score, label = analyze_sentiment(summary)
    st.subheader("📊 Analyse de sentiment")
    st.write(f"Tonalité détectée : **{label}** (score : {score:.2f})")

    wordcloud_path = generate_wordcloud(cleaned_text, doc_id)
    st.subheader("☁️ Nuage de mots")
    st.image(wordcloud_path, caption="Vocabulaire dominant")
    return wordcloud_path


def display_metadata(metadata):
    """Affichage des métadonnées d’un article extrait via URL"""
    st.subheader("ℹ️ Métadonnées de l’article")
    st.write(f"📰 Source : **{metadata.get('source', 'N/A')}**")
    st.write(f"🕓 Date : {metadata.get('publishedAt', 'N/A')}")
    if metadata.get("image_url"):
        st.image(metadata["image_url"], caption="Image d’illustration")


# === Interface principale ===

tab1, tab2 = st.tabs(["📄 Fichier PDF/DOCX", "🌍 Article en ligne"])

raw_text = None
metadata = {}
doc_id = None

with tab1:
    uploaded_file = st.file_uploader("Téléverser un fichier", type=["pdf", "docx"])
    if uploaded_file:
        doc_id = os.path.splitext(uploaded_file.name)[0]
        filepath = save_uploaded_file(uploaded_file)
        raw_text = extract_text_from_file(filepath)

with tab2:
    url = st.text_input("Coller l’URL d’un article d’actualité")
    if st.button("Extraire l’article depuis l’URL") and url:
        article_data = fetch_article_from_url(url)
        raw_text = article_data["text"]
        metadata = article_data["metadata"]
        doc_id = metadata.get("title", "article")

# === Pipeline IA ===
if raw_text:
    cleaned, chunks, index = process_text_pipeline(raw_text)

    st.markdown("---")
    st.markdown("## 🎯 Choisir le type de résumé")

    col1, col2 = st.columns(2)
    summary = ""

    with col1:
        if st.button("📄 Résumé classique"):
            summary = display_summary_section(chunks)

    with col2:
        theme = st.selectbox("🌍 Choisir un thème pour le résumé thématique", ["climat", "mobilisation citoyenne", "loi Duplomb"])
        if st.button("🌐 Résumé thématique"):
            summary = display_summary_section(chunks, thematic=True, theme=theme)

    if summary:
        wordcloud_path = display_analysis(summary, cleaned, doc_id)

        if metadata:
            display_metadata(metadata)

        st.markdown("---")
        st.subheader("📥 Export des résultats")
        st.download_button("💾 Télécharger le résumé (.txt)", summary, file_name=f"{doc_id}_resume.txt")
        st.download_button("💾 Télécharger le nuage de mots", open(wordcloud_path, "rb"), file_name=f"{doc_id}_cloud.png")
else:
    st.info("Uploade un fichier ou entre une URL pour commencer.")
     



