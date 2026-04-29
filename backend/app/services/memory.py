from datetime import datetime
from typing import Dict, Any

# -------- IN-MEMORY STORAGE --------
user_memory: Dict[str, Dict[str, Any]] = {}


# -------- GET CONTEXT --------
def get_user_context(user_id: str) -> Dict[str, Any]:
    if user_id not in user_memory:
        user_memory[user_id] = {
            "last_query": "",
            "history": [],
            "last_active": datetime.now()
        }
    return user_memory[user_id]


# -------- UPDATE LAST QUERY --------
def update_last_query(user_id: str, query: str):
    context = get_user_context(user_id)
    context["last_query"] = query
    context["last_active"] = datetime.now()


# -------- ADD CHAT HISTORY --------
def add_to_history(user_id: str, user_msg: str, bot_msg: str):
    context = get_user_context(user_id)

    context["history"].append({
        "user": user_msg,
        "bot": bot_msg,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    # 🔥 limit history size (memory safe)
    if len(context["history"]) > 20:
        context["history"] = context["history"][-20:]


# -------- GET HISTORY --------
def get_history(user_id: str):
    context = get_user_context(user_id)
    return context.get("history", [])


# -------- CLEAR MEMORY --------
def clear_user_memory(user_id: str):
    if user_id in user_memory:
        del user_memory[user_id]


# -------- CLEAN INACTIVE USERS --------
def cleanup_memory(timeout_minutes: int = 60):
    """
    Remove users inactive for given time
    """
    now = datetime.now()
    to_delete = []

    for user_id, data in user_memory.items():
        last_active = data.get("last_active", now)
        diff = (now - last_active).total_seconds() / 60

        if diff > timeout_minutes:
            to_delete.append(user_id)

    for user_id in to_delete:
        del user_memory[user_id]