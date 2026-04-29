from datetime import datetime

# ✅ CORRECT IMPORTS (VERY IMPORTANT)
from app.services.utils import get_time_greeting, clean_text
from app.services.math_handler import solve_math
from app.services.search import multi_source_answer
from app.services.memory import get_user_context
from app.services.nlp_engine import correct_text


# -------- CONTEXT RESOLUTION --------
def resolve_context(user_input, context):
    user_clean = clean_text(user_input)

    follow_words = ["it", "this", "that", "they", "he", "she"]

    if any(word in user_clean.split() for word in follow_words):
        if context.get("last_query"):
            return context["last_query"] + " " + user_input

    return user_input


# -------- INTENT DETECTION --------
def detect_intent(user_input):
    text = clean_text(user_input)

    if text.strip() in ["hello", "hi", "hey", "namaste"]:
        return "greeting"

    if "time" in text:
        return "time"

    if "date" in text:
        return "date"

    if any(op in text for op in ["+", "-", "*", "/", "sqrt", "sin", "cos", "tan", "power"]):
        return "math"

    if any(w in text for w in ["what", "who", "tell", "about", "define", "explain"]):
        return "search"

    return "unknown"


# -------- SMART FALLBACK --------
def smart_fallback(user_input):
    return (
        "I'm not fully sure what you mean 🤔.\n\n"
        "Try asking something like:\n"
        "• What is AI?\n"
        "• Tell me about black holes\n"
        "• Calculate sqrt 25"
    )


# -------- MAIN RESPONSE --------
def chatbot_response(user_input, user_id="default"):

    # 🔥 SPELL CORRECTION
    user_input = correct_text(user_input)

    context = get_user_context(user_id)
    intent = detect_intent(user_input)

    # -------- GREETING --------
    if intent == "greeting":
        return get_time_greeting()

    # -------- TIME --------
    if intent == "time":
        return datetime.now().strftime("Current time is %I:%M %p")

    # -------- DATE --------
    if intent == "date":
        return datetime.now().strftime("Today's date is %d %B %Y")

    # -------- MATH --------
    if intent == "math":
        result = solve_math(user_input)
        if result:
            return result
        return "I couldn't solve that math problem. Try a simpler expression."

    # -------- CONTEXT --------
    resolved = resolve_context(user_input, context)
    context["last_query"] = resolved

    # -------- SEARCH --------
    if intent == "search":
        result = multi_source_answer(resolved)

        if result and len(result.strip()) > 10:
            return result

        return "I couldn't find a clear answer. Try rephrasing your question."

    # -------- UNKNOWN --------
    return smart_fallback(user_input)


# -------- STREAMING RESPONSE --------
def chatbot_stream_response(user_input, user_id="default"):
    full_response = chatbot_response(user_input, user_id)

    # ✅ CHARACTER STREAMING (SMOOTH)
    for char in full_response:
        yield char