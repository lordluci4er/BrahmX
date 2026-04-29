from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.services.chatbot import chatbot_response, chatbot_stream_response

main = Blueprint("main", __name__)


# -------- HEALTH CHECK --------
@main.route("/")
def home():
    return jsonify({"status": "API Running"})


# -------- NORMAL RESPONSE API --------
@main.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message")
        user_id = data.get("user_id", "default")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        reply = chatbot_response(user_message, user_id)

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500


# -------- STREAMING RESPONSE API --------
@main.route("/chat-stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json()

        user_message = data.get("message")
        user_id = data.get("user_id", "default")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        def generate():
            try:
                for chunk in chatbot_stream_response(user_message, user_id):
                    yield chunk
            except Exception as e:
                yield f"\n⚠️ Error: {str(e)}"

        return Response(
            stream_with_context(generate()),
            mimetype="text/plain"
        )

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500