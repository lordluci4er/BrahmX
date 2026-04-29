user_memory = {}

def get_user_context(user_id):
    if user_id not in user_memory:
        user_memory[user_id] = {"last_query": ""}
    return user_memory[user_id]