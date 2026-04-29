import wikipedia
import requests
import re
from utils import extract_keywords
from nlp_engine import process_query, summarize_text_transformer


# -------- QUERY CLEANING --------
def clean_query(query):
    remove_phrases = [
        "tell me about", "what is", "who is",
        "define", "about", "explain"
    ]

    q = query.lower()

    for phrase in remove_phrases:
        q = q.replace(phrase, "")

    return q.strip()


# -------- OUTPUT CLEANING (STRONG VERSION) --------
def clean_output(text):
    # camelCase fix
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # punctuation spacing
    text = re.sub(r'([a-z])([.,])', r'\1 \2', text)

    # split merged words (strong fix)
    text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)

    # number join fix
    text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# -------- WIKIPEDIA --------
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=5)
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            return wikipedia.summary(e.options[0], sentences=3)
        except:
            return ""
    except:
        return ""


# -------- DUCKDUCKGO --------
def search_duckduckgo(query):
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}
        data = requests.get(url, params=params, timeout=3).json()

        if data.get("Abstract"):
            return data["Abstract"]

        related = data.get("RelatedTopics", [])
        if related:
            for item in related:
                if "Text" in item:
                    return item["Text"]

        return ""
    except:
        return ""


# -------- MULTI SOURCE (FINAL PIPELINE) --------
def multi_source_answer(query):

    # 🔥 STEP 1: NLP (spell + entity)
    corrected_query, entities = process_query(query)

    # 🔥 STEP 2: clean query
    clean_q = clean_query(corrected_query)

    # 🔥 STEP 3: entity priority
    if entities:
        clean_q = entities[0][0]

    # 🔥 STEP 4: fetch data
    wiki = search_wikipedia(clean_q)
    ddg = search_duckduckgo(clean_q)

    combined = " ".join([s for s in [wiki, ddg] if s])

    # 🔥 normalize BEFORE summarization (important)
    combined = re.sub(r'\s+', ' ', combined)

    # -------- TRANSFORMER SUMMARIZATION --------
    if combined.strip():
        summary = summarize_text_transformer(combined)

        if summary and len(summary.strip()) > 20:
            return clean_output(summary)

    # -------- FALLBACK --------
    if wiki and len(wiki) > 30:
        return clean_output(summarize_text_transformer(wiki))

    if ddg and len(ddg) > 30:
        return clean_output(summarize_text_transformer(ddg))

    return f"I couldn't find clear information about '{clean_q}'. Try asking differently."