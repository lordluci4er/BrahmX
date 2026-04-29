import re
from datetime import datetime
from typing import List, Dict


# -------- CLEAN TEXT --------
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    # remove special characters
    text = re.sub(r"[^\w\s]", " ", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -------- STOPWORDS (EXPANDED) --------
STOPWORDS = {
    "what","is","the","about","tell","me","who","are","a","an",
    "of","in","on","for","to","with","and","or","as","by",
    "does","do","did","how","why","when","where",
    "can","could","should","would","will","shall",
    "explain","define","give","information","details",
    "please","i","you","we","they","he","she","it",
    "this","that","these","those"
}


# -------- SIMPLE STEMMER --------
def simple_stem(word: str) -> str:
    suffixes = ["ing", "ed", "ly", "es", "s"]

    for suf in suffixes:
        if word.endswith(suf) and len(word) > len(suf) + 2:
            return word[:-len(suf)]

    return word


# -------- KEYWORD EXTRACTION --------
def extract_keywords(text: str) -> List[str]:
    text = clean_text(text)

    if not text:
        return []

    words = text.split()

    keywords = []

    for word in words:
        if word not in STOPWORDS and len(word) > 2:
            stemmed = simple_stem(word)
            keywords.append(stemmed)

    # remove duplicates (preserve order)
    seen = set()
    unique_keywords = []

    for w in keywords:
        if w not in seen:
            unique_keywords.append(w)
            seen.add(w)

    return unique_keywords


# -------- WEIGHTED KEYWORDS --------
def get_weighted_keywords(text: str) -> Dict[str, int]:
    keywords = extract_keywords(text)

    weights = {}

    for word in keywords:
        weights[word] = weights.get(word, 0) + 1

    return weights


# -------- TEXT NORMALIZER (NEW - VERY USEFUL) --------
def normalize_text(text: str) -> str:
    """
    Clean + lightweight normalization
    (used before NLP / search)
    """
    text = clean_text(text)

    # collapse repeated words (e.g. "ai ai ai")
    words = text.split()
    unique_words = []

    for w in words:
        if not unique_words or unique_words[-1] != w:
            unique_words.append(w)

    return " ".join(unique_words)


# -------- TIME GREETING --------
def get_time_greeting() -> str:
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Hello!"