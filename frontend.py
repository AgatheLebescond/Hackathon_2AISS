import os
import streamlit as st

from ingestion.extractor import extract_text_from_file
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text
from ingestion.processing.embedder import embed_chunks
from ingestion.processing.indexer import build_faiss_index, index_chunks
from ingestion.processing.summarizer import generate_summary  # , generate_thematic_summary
from ingestion.newsapi_fetcher import fetch_article_from_url

# === Configuration Streamlit
st.set_page_config(page_title="AI Résumeur", layout="wide")
st.title("🧠 Résumeur intelligent d'articles & PDF")

# ---------- Session state ----------
defaults = {
    "raw_text": None,
    "cleaned": None,
    "chunks": None,
    "index": None,
    "summary": None,
    "metadata": {},
    "doc_id": None,
    "auto_summarize": True,  # NEW: toggle to auto-generate summary after extraction
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# === Helpers ===
def save_uploaded_file(uploaded_file):
    filepath = os.path.join("data/uploads", uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
    return filepath

def process_text_pipeline(raw_text):
    cleaned = clean_text(raw_text)
    chunks = split_text(cleaned)
    embeddings = embed_chunks(chunks)
    embedding_dim = embeddings.shape[1]
    index = build_faiss_index(embedding_dim)
    index_chunks(index, embeddings)
    return cleaned, chunks, index

def run_pipeline_and_store(text, doc_id=None, metadata=None):
    cleaned, chunks, index = process_text_pipeline(text)
    st.session_state.raw_text = text
    st.session_state.cleaned = cleaned
    st.session_state.chunks = chunks
    st.session_state.index = index
    st.session_state.doc_id = doc_id or "document"
    st.session_state.metadata = metadata or {}

def display_summary_section(chunks, thematic=False, theme=None):
    """Affichage d’un résumé généré automatiquement"""
    with st.spinner("Génération du résumé..."):
        if thematic and theme:
            # summary = generate_thematic_summary(chunks, theme=theme)
            summary = generate_summary(chunks)
            st.subheader(f"🌍 Résumé thématique : {theme}")
        else:
            summary = generate_summary(chunks)
            st.subheader("📝 Résumé généré")
    st.success(summary)
    return summary

def display_metadata(metadata):
    st.subheader("ℹ️ Métadonnées de l’article")
    st.write(f"📰 Source : **{metadata.get('source', 'N/A')}**")
    st.write(f"🕓 Date : {metadata.get('publishedAt', 'N/A')}")
    if metadata.get("image_url"):
        st.image(metadata["image_url"], caption="Image d’illustration")

# === Interface principale ===
tab1, tab2, tab3 = st.tabs(["📄 Fichier PDF/DOCX", "🌍 Article en ligne", "🧾 Résultats"])

with tab1:
    st.checkbox(
        "Générer automatiquement un résumé après l'extraction",
        key="auto_summarize",
        help="Si coché, le résumé est produit dès que l'article/le fichier est chargé."
    )
    uploaded_file = st.file_uploader("Téléverser un fichier", type=["pdf", "docx"], key="file_uploader")
    if uploaded_file:
        doc_id = os.path.splitext(uploaded_file.name)[0]
        filepath = save_uploaded_file(uploaded_file)
        text = extract_text_from_file(filepath)
        run_pipeline_and_store(text, doc_id=doc_id, metadata={})
        st.success("Fichier chargé.")
        if st.session_state.auto_summarize and st.session_state.chunks:
            st.session_state.summary = display_summary_section(st.session_state.chunks)

with tab2:
    url = st.text_input("Coller l’URL d’un article d’actualité", key="url_input")
    if st.button("Extraire l’article depuis l’URL", key="fetch_url") and url:
        try:
            st.markdown("Fetcher…")
            article_data = fetch_article_from_url(url, api_token="00d1111a7e584642bf066fb39c6746b8")
            text = article_data.get('text', '') or ''
            meta = article_data.get('metadata', {}) or {}
            doc_id = meta.get('title', 'article')
            if not text.strip():
                st.warning("Aucun texte n’a été extrait depuis l’URL.")
            run_pipeline_and_store(text, doc_id=doc_id, metadata=meta)
            st.success("Article extrait.")
            if st.session_state.auto_summarize and st.session_state.chunks:
                st.session_state.summary = display_summary_section(st.session_state.chunks)
        except Exception as e:
            st.error(f"Erreur lors de l’extraction : {e}")

    # Boutons de génération manuelle
    if st.session_state.chunks:
        st.markdown("---")
        st.markdown("## 🎯 Choisir le type de résumé")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Résumé classique", key="classic_summary"):
                st.session_state.summary = display_summary_section(st.session_state.chunks)
        with col2:
            theme = st.selectbox(
                "🌍 Choisir un thème pour le résumé thématique",
                ["climat", "mobilisation citoyenne", "loi Duplomb"],
                key="theme_select"
            )
            if st.button("🌐 Résumé thématique", key="thematic_summary"):
                st.session_state.summary = display_summary_section(
                    st.session_state.chunks, thematic=True, theme=theme
                )

with tab3:
    st.markdown("## 🧾 Résultats")
    # Résumé (toujours affiché s'il existe)
    if st.session_state.summary:
        st.subheader("📝 Résumé")
        st.text_area("Résumé généré", st.session_state.summary, height=280)
        st.download_button(
            "💾 Télécharger le résumé (.txt)",
            st.session_state.summary,
            file_name=f"{st.session_state.doc_id or 'document'}_resume.txt",
            key="download_summary"
        )
    else:
        st.info("Aucun résumé pour l’instant. Importez un contenu et générez un résumé.")

    # Métadonnées (si disponibles)
    if st.session_state.metadata:
        st.markdown("---")
        display_metadata(st.session_state.metadata)

    # Diagnostics utiles
    if st.session_state.cleaned or st.session_state.chunks:
        st.markdown("---")
        st.subheader("🔎 Diagnostics")
        c1, c2, c3 = st.columns(3)
        if st.session_state.cleaned:
            c1.metric("Mots (texte nettoyé)", len(st.session_state.cleaned.split()))
        if st.session_state.chunks:
            c2.metric("Nombre de chunks", len(st.session_state.chunks))
            # aperçu du 1er chunk
            with st.expander("Aperçu du 1er chunk"):
                st.code(st.session_state.chunks[0][:1000])
        if st.session_state.index:
            c3.write("Index FAISS : **OK**")

# Message d’accueil si rien encore
if not (st.session_state.raw_text or st.session_state.chunks or st.session_state.summary):
    st.info("Téléverse un fichier ou entre une URL pour commencer.")

# Commentaires du code

## 1. Imports

```python
import os
import streamlit as st
os : pour manipuler les chemins de fichiers.
streamlit : bibliothèque pour créer une application web interactive avec Python.
from ingestion.extractor import extract_text_from_file
#Fonction personnalisée pour extraire le texte d’un fichier (PDF ou DOCX).
from ingestion.cleaner import clean_text
#Fonction de nettoyage : supprime les caractères inutiles, normalise le texte.
from ingestion.processing.splitter import split_text
#Découpe le texte long en morceaux plus petits (chunks) pour traitement vectoriel.
from ingestion.processing.embedder import embed_chunks
#Génère des représentations vectorielles (embeddings) à partir des chunks.
from ingestion.processing.indexer import build_faiss_index, index_chunks
#Crée un index FAISS (recherche sémantique rapide) et y insère les vecteurs.
from ingestion.processing.summarizer import generate_summary
#Fonction qui utilise un modèle de langage pour résumer automatiquement le texte.
from ingestion.newsapi_fetcher import fetch_article_from_url
#Fonction qui récupère le contenu d’un article en ligne via une API.

2. Configuration de la page Streamlit
st.set_page_config(page_title="AI Résumeur", layout="wide")
#Définit le titre et le layout élargi pour l’interface.
st.title("🧠 Résumeur intelligent d'articles & PDF")
#Affiche le titre principal dans l’interface.

3. Initialisation du session_state
defaults = { ... }
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
#Ce bloc initialise des variables persistantes pour mémoriser les étapes entre les actions utilisateur :
texte brut, texte nettoyé, résumé, chunks, index, etc.

4. Sauvegarde du fichier uploadé
def save_uploaded_file(uploaded_file):
    ...
#Enregistre localement les fichiers uploadés dans un dossier data/uploads/.

5. Pipeline de traitement texte
def process_text_pipeline(raw_text):
    ...
#Nettoie le texte,
#Découpe en chunks,
#Génère les embeddings,
#Crée et alimente un index FAISS.

6. Stockage des résultats dans la session
def run_pipeline_and_store(text, doc_id=None, metadata=None):
    ...
#Stocke tous les résultats intermédiaires dans st.session_state pour être utilisés dans les onglets suivants.

7. Génération du résumé
def display_summary_section(chunks, thematic=False, theme=None):
    ...
#Affiche un résumé automatique (thématique ou non),
#Utilise la fonction generate_summary() pour créer un résumé textuel à partir des chunks.

8. Affichage des métadonnées
def display_metadata(metadata):
    ...
#Affiche les informations associées à un article (source, date, image), si disponibles.

9. Interface principale Onglets
tab1, tab2, tab3 = st.tabs(["📄 Fichier PDF/DOCX", "🌍 Article en ligne", "🧾 Résultats"])
#Organisation de l’interface en 3 onglets :
tab1 : upload de fichiers,
tab2 : extraction depuis une URL,
tab3 : résumé et diagnostic.

10. Onglet 1  Upload de fichier
with tab1:
    ...
#L’utilisateur téléverse un fichier local,
#Le texte est extrait, puis traité avec le pipeline complet,
#Si la case est cochée (auto_summarize), le résumé est généré automatiquement.

11. Onglet 2  Extraction d’article via URL
with tab2:
    ...
#L’utilisateur colle une URL d’article,
#Le texte est extrait via NewsAPI,
#Stockage des résultats et affichage du résumé,
#Option de choisir un thème de résumé.

12. Onglet 3  Résultats
with tab3:
    ...
#Affichage du résumé généré (si disponible),
#Téléchargement du résumé (.txt),
#Affichage des métadonnées,
#Affichage de diagnostics techniques :
#nombre de mots,
#nombre de chunks,
#vérification FAISS,
#aperçu du premier chunk.

13. Message d’accueil
if not (st.session_state.raw_text or st.session_state.chunks or st.session_state.summary):
    st.info("Téléverse un fichier ou entre une URL pour commencer.")
#Message affiché si l’application n’a encore reçu aucun contenu.

---------
