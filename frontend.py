import os
import streamlit as st

from ingestion.extractor import extract_text_from_file
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text
from ingestion.processing.embedder import embed_chunks
from ingestion.processing.indexer import build_faiss_index, search_top_k
from ingestion.processing.summarizer import generate_summary
from ingestion.processing.sentiment_analyzer import analyze_sentiment
from ingestion.processing.wordcloud_generator import generate_wordcloud
from ingestion.newsapi_fetcher import fetch_article_from_url

st.set_page_config(page_title="AI Résumeur", layout="wide")

st.title("🧠 Résumeur intelligent d'articles & PDF")

# --- UPLOAD FICHIER OU URL ---
tab1, tab2 = st.tabs(["📄 Fichier PDF/DOCX", "🌍 Article en ligne"])

with tab1:
    uploaded_file = st.file_uploader("Téléverser un fichier", type=["pdf", "docx"])
    if uploaded_file:
        doc_id = os.path.splitext(uploaded_file.name)[0]
        filepath = f"data/uploads/{uploaded_file.name}"
        with open(filepath, "wb") as f:
            f.write(uploaded_file.read())
        raw_text = extract_text_from_file(filepath)

with tab2:
    url = st.text_input("Coller l’URL d’un article d’actualité")
    if st.button("Extraire l’article depuis l’URL") and url:
        article_data = fetch_article_from_url(url)
        raw_text = article_data["text"]
        metadata = article_data["metadata"]
        doc_id = metadata.get("title", "article")

# --- TRAITEMENT ---
if 'raw_text' in locals():
    cleaned = clean_text(raw_text)
    chunks = split_text(cleaned)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)

    # Résumé automatique
    summary = generate_summary(chunks)
    st.markdown("### 📝 Résumé généré")
    st.success(summary)

    # Analyse de sentiment
    score, label = analyze_sentiment(summary)
    st.markdown("### 📊 Analyse de sentiment")
    st.write(f"**Tonalité détectée :** {label} (score : {score:.2f})")

    # Nuage de mots
    wordcloud_path = generate_wordcloud(cleaned, doc_id)
    st.markdown("### ☁️ Nuage de mots")
    st.image(wordcloud_path, caption="Vocabulaire dominant")

    # Métadonnées
    if 'metadata' in locals():
        st.markdown("### ℹ️ Métadonnées de l’article")
        st.write(f"📰 Source : **{metadata.get('source', 'N/A')}**")
        st.write(f"🕓 Date : {metadata.get('publishedAt', 'N/A')}")
        if metadata.get("image_url"):
            st.image(metadata["image_url"], caption="Image d’illustration")

    # Exports
    st.download_button("💾 Télécharger le résumé", summary, file_name=f"{doc_id}_resume.txt")
    st.download_button("💾 Télécharger le nuage de mots", open(wordcloud_path, "rb"), file_name=f"{doc_id}_wordcloud.png")

else:
    st.info("Uploade un fichier ou entre une URL pour commencer.")



