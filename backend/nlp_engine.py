from symspellpy import SymSpell
import spacy
import pkg_resources
import re
from transformers import pipeline

# -------- LOAD SPACY --------
nlp = spacy.load("en_core_web_sm")

# -------- LOAD SYMSPELL --------
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)

sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# -------- TRANSFORMER (LAZY LOAD) --------
hf_summarizer = None

def load_hf_model():
    global hf_summarizer
    if hf_summarizer is None:
        hf_summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=-1
        )

# -------- SPELL CORRECTION --------
def correct_text(text):
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    return suggestions[0].term if suggestions else text

# -------- FIX SPACING (STRONG VERSION) --------
def fix_spacing(text):
    # camelCase fix
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # punctuation spacing
    text = re.sub(r'([a-z])([.,])', r'\1 \2', text)

    # word boundary fix (important)
    text = re.sub(r'([a-z])([A-Z][a-z])', r'\1 \2', text)

    # number join fix
    text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# -------- TOKENIZER --------
def tokenize_text(text):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_punct]

# -------- ENTITY EXTRACTION --------
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# -------- NLP CLEANUP --------
def clean_text_nlp(text):
    text = fix_spacing(text)

    doc = nlp(text)

    clean_tokens = [
        token.text for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(clean_tokens)

# -------- SPACY SUMMARIZER --------
def summarize_text(text, max_sentences=3):

    text = fix_spacing(text)
    doc = nlp(text)

    sentence_scores = {}

    for sent in doc.sents:
        score = 0

        for token in sent:
            if not token.is_stop and not token.is_punct:
                score += 1

        length = len(sent)
        if length > 0:
            score = score / length

        sentence_scores[sent.text.strip()] = score

    sorted_sentences = sorted(
        sentence_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best = [s[0] for s in sorted_sentences[:max_sentences]]

    return " ".join(best)

# -------- TRANSFORMER SUMMARIZER (FIXED) --------
def summarize_text_transformer(text):
    try:
        load_hf_model()

        text = fix_spacing(text)
        text = text[:2000]

        input_len = len(text.split())

        # 🔥 dynamic length fix (important)
        max_len = min(120, int(input_len * 0.6))
        min_len = max(20, int(input_len * 0.3))

        summary = hf_summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        return summary[0]["summary_text"]

    except Exception:
        return summarize_text(text)

# -------- MAIN PROCESS --------
def process_query(query):
    corrected = correct_text(query)
    entities = extract_entities(corrected)
    return corrected, entities