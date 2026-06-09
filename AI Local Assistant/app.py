"""
Flask web UI for Hassan's AI Chatbot.
Streams Ollama responses token-by-token via Server-Sent Events.
"""
import json
from flask import Flask, render_template, Response, request, jsonify

from chatbot import SmartChatbot

app = Flask(__name__)

bot = SmartChatbot()

@app.route("/")
def index():
    return render_template("index.html", bot_name=bot.name, model=bot.model)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "empty message"}), 400

    def generate():
        try:
            for chunk in bot.stream(user_message):
                payload = json.dumps({"content": chunk})
                yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(generate(), mimetype="text/event-stream")


@app.route("/api/new_chat", methods=["POST"])
def new_chat():
    bot.clear_history()
    return jsonify({"ok": True, "history": []})


@app.route("/api/save", methods=["POST"])
def save_chat():
    filename = bot.save_history()
    return jsonify({"ok": True, "filename": filename})


@app.route("/api/history", methods=["GET"])
def get_history():
    return jsonify({"history": bot.get_history()})


if __name__ == "__main__":
    # threaded=True so the SSE stream isn't blocked by other requests
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
