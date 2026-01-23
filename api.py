from flask import Flask, request, jsonify, Response
from rag.rag_query import answer, stream_answer

app = Flask(__name__)

# Simple in-memory chat history
chat_history = []

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Store conversation history (last 5 messages)
    chat_history.append({"role": "user", "content": question})
    recent_history = chat_history[-5:]

    # Build conversation context
    context = "\n".join([msg["content"] for msg in recent_history])

    try:
        response = answer(context)

        chat_history.append({"role": "assistant", "content": response})

        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stream", methods=["POST"])
def stream():
    data = request.json
    question = data.get("question")

    if not question:
        return Response("No question provided", status=400)

    def generate():
        for token in stream_answer(question):
            yield token

    return Response(generate(), mimetype="text/plain")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    print("\n ERPNext Code Intelligence AI Backend")
    print(" Server running at: http://localhost:8000")
    print("📡 Endpoints:")
    print("   POST /ask     → Normal chat")
    print("   POST /stream  → Streaming chat")
    print("   GET  /health  → Health check\n")

    app.run(host="0.0.0.0", port=8000, debug=True)
