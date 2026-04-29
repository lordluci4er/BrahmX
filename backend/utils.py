import re
from datetime import datetime

# -------- CLEAN TEXT --------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
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
def simple_stem(word):
    # basic suffix removal (lightweight)
    suffixes = ["ing", "ed", "ly", "es", "s"]
    for suf in suffixes:
        if word.endswith(suf) and len(word) > len(suf) + 2:
            return word[:-len(suf)]
    return word


# -------- KEYWORD EXTRACTION --------
def extract_keywords(text):
    text = clean_text(text)
    words = text.split()

    keywords = []

    for word in words:
        if word not in STOPWORDS and len(word) > 2:
            stemmed = simple_stem(word)
            keywords.append(stemmed)

    # remove duplicates but keep order
    seen = set()
    unique_keywords = []
    for w in keywords:
        if w not in seen:
            unique_keywords.append(w)
            seen.add(w)

    return unique_keywords


# -------- BONUS: IMPORTANT WORD BOOST --------
def get_weighted_keywords(text):
    keywords = extract_keywords(text)

    weights = {}
    for word in keywords:
        weights[word] = weights.get(word, 0) + 1

    return weights


# -------- TIME GREETING --------
def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Hello!"