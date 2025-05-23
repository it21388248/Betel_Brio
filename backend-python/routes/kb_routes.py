from flask import Blueprint, request, jsonify
from utils.pinecone_handler import retrieve_kb_answer

kb_bp = Blueprint("kb", __name__)

@kb_bp.route("/ask", methods=["POST", "OPTIONS"])
def ask_kb():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        data = request.get_json(force=True)
        message = data.get("message", "")

        if not message:
            return jsonify({"reply": "⚠️ Please provide a valid question."}), 400

        answer = retrieve_kb_answer(message)
        return jsonify({"reply": answer})
    except Exception as e:
        print("❌ Error in /kb/ask:", e)
        return jsonify({"reply": f"⚠️ Error: {str(e)}"}), 500
