# pages/02_LoiDuplomb_Monitor.py
import os
import json
import time
import requests
import random
from datetime import datetime, timedelta, timezone

import streamlit as st

# Reuse your pipeline piece
from ingestion.cleaner import clean_text
from ingestion.processing.splitter import split_text
from ingestion.processing.summarizer import generate_summary
from ingestion.newsapi_fetcher import fetch_article_from_url  # uses your NewsAPI/extractor

# -------------------- Config --------------------
st.set_page_config(page_title="Veille Loi Duplomb", layout="wide")
st.title("🛰️ Veille automatique — Loi Duplomb")

NEWSAPI_KEY = "00d1111a7e584642bf066fb39c6746b8"
PUSHOVER_TOKEN = "akdgjtky9cwgcqr93rvc39o6a1fi88"
PUSHOVER_USER = "ujz194dfzvqe5m2ef1kwy8fyxeq3km"

SEEN_PATH = "data/monitor_seen.json"
os.makedirs("data", exist_ok=True)

# -------------------- Session State --------------------
defaults = {
    "monitor_enabled": False,
    "last_run": None,
    "interval_secs": 180,  # default 3 minutes
    "preview_only": True,  # dry run by default
    "max_items_per_run": 3,
    "last_found": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------- Utilities --------------------
def load_seen():
    if not os.path.exists(SEEN_PATH):
        return set()
    try:
        with open(SEEN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return set(data)
    except Exception:
        return set()

def save_seen(seen_set):
    try:
        with open(SEEN_PATH, "w", encoding="utf-8") as f:
            json.dump(sorted(list(seen_set)), f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"Impossible de sauvegarder le cache des articles vus: {e}")

def summarize_text(text: str) -> str:
    cleaned = clean_text(text or "")
    chunks = split_text(cleaned)
    if not chunks:
        return ""
    return generate_summary(chunks)

def send_pushover(title: str, message: str, url: str = None):
    if st.session_state.preview_only:
        return {"status": "preview", "info": "Notification non envoyée (mode aperçu)."}
    if not (PUSHOVER_TOKEN and PUSHOVER_USER):
        raise RuntimeError("Clés Pushover absentes (PUSHOVER_TOKEN / PUSHOVER_USER).")
    payload = {
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "title": title[:250] if title else "Veille Loi Duplomb",
        "message": message[:1024],  # Pushover hard limit
        "priority": 0,
    }
    if url:
        payload["url"] = url
        payload["url_title"] = "Ouvrir l’article"
    r = requests.post("https://api.pushover.net/1/messages.json", data=payload, timeout=20)
    r.raise_for_status()
    return r.json()

def newsapi_search(query: str, from_dt: datetime, page_size: int = 20):
    """
    Lightweight NewsAPI /v2/everything call.
    Returns list of articles (dicts). We rely on your fetcher for full text later.
    """
    if not NEWSAPI_KEY:
        raise RuntimeError("Clé NewsAPI absente (NEWS_API_TOKEN).")
    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "fr",
        "sortBy": "publishedAt",
        "from": from_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "pageSize": page_size,
        "apiKey": NEWSAPI_KEY,
    }
    r = requests.get(endpoint, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("articles", []) or []

def safe_title(a: dict) -> str:
    return (a.get("title") or a.get("description") or "Article").strip()

def safe_id(a: dict) -> str:
    # Build a stable ID from url+publishedAt
    return f"{a.get('url','')}|{a.get('publishedAt','')}"

def fetch_and_summarize_article(url: str) -> tuple[str, str]:
    """
    Uses your extractor to get full text, then summarize.
    Returns (summary, raw_text)
    """
    try:
        data = fetch_article_from_url(url, api_token=os.getenv("NEWS_API_TOKEN", ""))  # reuse same key if your fetcher needs it
        text = (data.get("text") or "").strip()
        if not text:
            return "", ""
        summary = summarize_text(text)
        return summary, text
    except Exception as e:
        st.warning(f"Extraction échouée pour {url}: {e}")
        return "", ""

def monitor_once():
    """
    One polling cycle:
    - query NewsAPI
    - deduplicate vs. seen
    - extract+summarize each new article
    - send pushover
    """
    # search window (avoid heavy queries): last 24h
    now_utc = datetime.now(timezone.utc)
    window_from = now_utc - timedelta(hours=24)

    try:
        articles = newsapi_search('\"loi duplomb\" OR (loi AND duplomb)', window_from, page_size=20)
    except Exception as e:
        st.error(f"Erreur NewsAPI: {e}")
        return []

    seen = load_seen()
    new_items = []
    for a in articles:
        aid = safe_id(a)
        if aid in seen:
            continue
        new_items.append(a)

    # Limit per run to avoid bursts
    new_items = new_items[: st.session_state.max_items_per_run]

    delivered = []
    for a in new_items:
        url = a.get("url")
        title = safe_title(a)
        source = (a.get("source") or {}).get("name") or "Source"
        published = a.get("publishedAt") or ""
        header = f"{title} — {source}"
        # Get full text + summary
        summary, raw = fetch_and_summarize_article(url)
        if not summary and (a.get("description") or a.get("content")):
            # fallback to available newsapi fields
            summary = (a.get("description") or a.get("content") or "").strip()

        msg_lines = [
            f"{summary}" if summary else "(pas de résumé disponible)",
            "",
            f"Publié: {published}",
        ]
        message = "\n".join([ln for ln in msg_lines if ln is not None])
        try:
            resp = send_pushover(header, message, url=url)
            delivered.append({
                "title": title,
                "source": source,
                "publishedAt": published,
                "url": url,
                "status": "sent" if not st.session_state.preview_only else "preview",
                "pushover_resp": resp,
            })
        except Exception as e:
            st.error(f"Pushover non envoyé pour “{title}”: {e}")

        # mark as seen whether or not push succeeded, to avoid loops on bad tokens
        seen.add(safe_id(a))

    save_seen(seen)
    return delivered

# -------------------- Sidebar Controls --------------------
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.session_state.interval_secs = st.slider("Intervalle de rafraîchissement (sec)", 30, 900, st.session_state.interval_secs, 10)
    st.session_state.max_items_per_run = st.slider("Max articles par cycle", 1, 10, st.session_state.max_items_per_run, 1)
    st.session_state.preview_only = st.toggle("Mode aperçu (ne pas envoyer sur Pushover)", value=st.session_state.preview_only)
    colA, colB = st.columns(2)
    with colA:
        if st.button("▶️ Démarrer"):
            st.session_state.monitor_enabled = True
    with colB:
        if st.button("⏹️ Arrêter"):
            st.session_state.monitor_enabled = False

    st.caption(f"NEWSAPI_TOKEN set: {'✅' if bool(NEWSAPI_KEY) else '❌'} | Pushover set: {'✅' if PUSHOVER_TOKEN and PUSHOVER_USER else '❌'}")

# -------------------- Auto-refresh --------------------
# When enabled, this triggers full reruns at the chosen interval (non-blocking).
if st.session_state.monitor_enabled:
    st_autorefresh = st.rerun  # fallback alias if older Streamlit
    st_autorefresh = st.autorefresh if hasattr(st, "autorefresh") else None
    if st_autorefresh:
        st_autorefresh(interval=st.session_state.interval_secs * 1000, key="monitor_refresh")

# -------------------- Main Run --------------------
st.markdown("### État du moniteur")
if st.session_state.monitor_enabled:
    st.success(f"Actif — vérification toutes les {st.session_state.interval_secs} secondes.")
else:
    st.info("Inactif.")

# Run one monitoring cycle each time the page loads (if enabled)
results = []
if st.session_state.monitor_enabled:
    with st.spinner("Recherche de nouveaux articles…"):
        results = monitor_once()
    st.session_state.last_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Dernière exécution", st.session_state.last_run or "—")
c2.metric("Nouveaux articles ce cycle", len(results))
c3.metric("Mode", "APERÇU" if st.session_state.preview_only else "ENVOI")

if results:
    st.markdown("### Nouveautés")
    for item in results:
        with st.expander(f"📰 {item['title']} — {item['source']} ({item['status']})"):
            st.write(f"Publié : {item['publishedAt']}")
            st.write(item["url"])
else:
    st.caption("Aucune nouveauté lors de ce cycle (ou moniteur arrêté).")

# -------------------- NewsAPI utils génériques --------------------
def newsapi_everything(
    query: str,
    from_dt: datetime,
    to_dt: datetime,
    *,
    language: str = "fr",
    sort_by: str = "publishedAt",
    page: int = 1,
    page_size: int = 20,
    search_in: str = "title,description,content",  # <-- AJOUT
) -> dict:
    """
    Appelle /v2/everything et renvoie le JSON complet (incluant totalResults).
    """
    if not NEWSAPI_KEY:
        raise RuntimeError("Clé NewsAPI absente (NEWSAPI_KEY).")

    endpoint = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": language,
        "sortBy": sort_by,
        "from": from_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "to": to_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "page": page,
        "pageSize": page_size,
        "searchIn": search_in,  # <-- AJOUT
        "apiKey": NEWSAPI_KEY,
    }
    r = requests.get(endpoint, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def pick_random_article_from_window(
    query: str,
    from_dt: datetime,
    to_dt: datetime,
    *,
    language: str = "fr"
) -> dict | None:
    """
    Tire au hasard un article dans la fenêtre temporelle.
    On borne volontairement à ~100 premiers résultats accessibles.
    """
    meta = newsapi_everything(query, from_dt, to_dt, language=language, page=1, page_size=1)
    total = int(meta.get("totalResults") or 0)
    if total <= 0:
        return None

    HARD_CAP = 100
    capped_total = min(total, HARD_CAP)
    page_size = 20

    global_idx = random.randint(0, capped_total - 1)
    page = (global_idx // page_size) + 1
    within_page_idx = global_idx % page_size

    batch = newsapi_everything(query, from_dt, to_dt, language=language, page=page, page_size=page_size)
    articles = batch.get("articles") or []
    if not articles:
        return None

    return articles[within_page_idx % len(articles)]

def get_random_article_last_month_climat_loi_pesticides_france() -> dict | None:
    """
    Article aléatoire des 30 derniers jours contenant:
    climat AND loi AND pesticides AND France
    """
    now_utc = datetime.now(timezone.utc)
    from_dt = now_utc - timedelta(days=30)
    to_dt = now_utc

    # Requête stricte avec AND sur les 4 mots-clés
    q = "(climat) AND (loi) AND (pesticides) AND (France)"
    return pick_random_article_from_window(q, from_dt, to_dt, language="fr")

# -------------------- Bouton UI : test aléatoire climat/loi/pesticides/France --------------------
with st.sidebar:
    st.markdown("---")
    if st.button("🎲 Test Pushover — climat/loi/pesticides/France (30j)"):
        try:
            a = get_random_article_last_month_climat_loi_pesticides_france()
            if not a:
                st.warning("Aucun article correspondant sur les 30 derniers jours.")
            else:
                url = a.get("url")
                title = safe_title(a)
                source = (a.get("source") or {}).get("name") or "Source"
                published = a.get("publishedAt") or ""

                summary, raw = fetch_and_summarize_article(url)
                if not summary and (a.get("description") or a.get("content")):
                    summary = (a.get("description") or a.get("content") or "").strip()

                header = f"{title} — {source}"
                message = "\n".join(filter(None, [
                    summary if summary else "(pas de résumé disponible)",
                    "",
                    f"Publié: {published}",
                ]))

                resp = send_pushover(header, message, url=url)
                st.session_state.last_found = [a]
                st.success(f"Test {'(aperçu)' if st.session_state.preview_only else ''} envoyé: {title}")
        except Exception as e:
            st.error(f"Échec du test aléatoire: {e}")