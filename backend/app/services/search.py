import wikipedia
import requests
import re
from typing import Tuple, List

# ✅ FIXED IMPORTS
from app.services.utils import extract_keywords
from app.services.nlp_engine import process_query, summarize_text_transformer


# -------- QUERY CLEANING --------
def clean_query(query: str) -> str:
    if not query:
        return ""

    remove_phrases = [
        "tell me about", "what is", "who is",
        "define", "about", "explain"
    ]

    q = query.lower()

    for phrase in remove_phrases:
        q = q.replace(phrase, "")

    return q.strip()


# -------- OUTPUT CLEANING --------
def clean_output(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([a-z])([.,])', r'\1 \2', text)
    text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)
    text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# -------- WIKIPEDIA --------
def search_wikipedia(query: str) -> str:
    try:
        return wikipedia.summary(query, sentences=5)
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            return wikipedia.summary(e.options[0], sentences=3)
        except Exception:
            return ""
    except Exception:
        return ""


# -------- DUCKDUCKGO --------
def search_duckduckgo(query: str) -> str:
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}

        response = requests.get(url, params=params, timeout=3)

        if response.status_code != 200:
            return ""

        data = response.json()

        if data.get("Abstract"):
            return data["Abstract"]

        related = data.get("RelatedTopics", [])
        for item in related:
            if isinstance(item, dict) and "Text" in item:
                return item["Text"]

        return ""

    except Exception:
        return ""


# -------- MULTI SOURCE (FINAL FIXED) --------
def multi_source_answer(query: str) -> str:

    # 🔥 STEP 1: NLP (spell + entity)
    corrected_query, entities = process_query(query)

    # 🔥 STEP 2: clean query
    clean_q = clean_query(corrected_query)

    # 🔥 STEP 3: entity priority (FIXED)
    if entities:
        clean_q = entities[0][0].lower()

    # 🔥 EXTRA CLEAN (VERY IMPORTANT)
    clean_q = clean_q.replace("about", "").strip()

    # 🔥 STEP 4: fetch data
    wiki = search_wikipedia(clean_q)
    ddg = search_duckduckgo(clean_q)

    combined = " ".join([s for s in [wiki, ddg] if s])

    # 🔥 normalize text
    combined = re.sub(r'\s+', ' ', combined)

    # 🔥 LIMIT TEXT (CRITICAL FIX)
    combined = combined[:1500]

    # -------- TRANSFORMER SUMMARIZATION --------
    if combined.strip():
        try:
            summary = summarize_text_transformer(combined)

            if summary and len(summary.strip()) > 20:
                return clean_output(summary)

        except Exception:
            pass

    # -------- FALLBACK --------
    if wiki and len(wiki) > 30:
        return clean_output(wiki[:300])

    if ddg and len(ddg) > 30:
        return clean_output(ddg[:300])

    return f"I couldn't find clear information about '{clean_q}'. Try asking differently."