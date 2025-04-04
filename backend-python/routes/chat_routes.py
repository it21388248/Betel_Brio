from flask import Blueprint, request, jsonify
from utils.predictor import predict_price
from utils.embeddings import get_embedding
from utils.pinecone_handler import query_pinecone
from openai import OpenAI
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()
chat_bp = Blueprint("chat", __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sessions = defaultdict(dict)

price_fields = ["Date", "Leaf_Type", "Leaf_Size", "Quality_Grade", "No_of_Leaves", "Location", "Season"]
price_questions = {
    "Date": "📅 What is the date? (YYYY-MM-DD)",
    "Leaf_Type": "🌿 What is the leaf type?",
    "Leaf_Size": "📏 What is the leaf size?",
    "Quality_Grade": "✅ What is the quality grade?",
    "No_of_Leaves": "🍃 How many leaves do you have?",
    "Location": "📍 What is your location?",
    "Season": "🗓️ What season is it?"
}

@chat_bp.route("/", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        session_id = data.get("session_id", "default")
        session = sessions[session_id]

        # Greeting with carousel options
        if message.lower() in ["hi", "hello", "hey"]:
            sessions[session_id] = {}  # Reset session
            return jsonify({
                "reply": "👋 Hello! I'm BetelBrio — your assistant for betel insights. What would you like to do?",
                "options": [
                    {"label": "📈 Price Prediction", "value": "start price prediction"},
                    {"label": "💬 Ask a Question", "value": "ask question"}
                ]
            })

        # Price prediction flow
        if message.lower() == "start price prediction" or session.get("collecting_price"):
            session["collecting_price"] = True

            # Store previous field answer
            current_field = session.get("current_price_field")
            if current_field:
                session[current_field] = message

            # Ask next field question
            for field in price_fields:
                if field not in session:
                    session["current_price_field"] = field
                    return jsonify({"reply": price_questions[field]})

            # All fields collected — run model
            try:
                predicted_price = predict_price(
                    session["Date"],
                    session["Leaf_Type"],
                    session["Leaf_Size"],
                    session["Quality_Grade"],
                    int(session["No_of_Leaves"]),
                    session["Location"],
                    session["Season"]
                )
                sessions.pop(session_id, None)  # Clear session
                return jsonify({"reply": f"💰 Predicted price per leaf: **{predicted_price}**"})
            except Exception as e:
                return jsonify({"reply": f"⚠️ Error predicting price: {str(e)}"}), 500

        # Free-form question handler
        if message.lower() == "ask question":
            return jsonify({
                "reply": "🧠 Sure! Ask me anything related to betel farming or insights from the knowledge base."
            })

        # Fallback to knowledge base (Pinecone + GPT)
        embedding = get_embedding(message)
        context = query_pinecone(embedding)
        if not context:
            return jsonify({
                "reply": "⚠️ I can only answer based on the uploaded knowledge base or assist with predictions like price or demand."
            })

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are BetelBrio, a smart assistant who helps users with betel predictions "
                        "and answers based on uploaded documents."
                    )
                },
                {
                    "role": "user",
                    "content": f"Question: {message}\n\nContext: {context}"
                }
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        print("❌ Error in chat route:", e)
        return jsonify({"error": str(e)}), 500
