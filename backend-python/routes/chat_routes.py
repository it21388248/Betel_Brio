from flask import Blueprint, request, jsonify
from utils.predictor import predict_price
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()
chat_bp = Blueprint("chat", __name__)
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

        # Free-form question handler (redirects to /kb/ask)
        if message.lower() == "ask question":
            return jsonify({
                "reply": "🧠 Sure! Ask me anything related to betel farming or insights from the knowledge base.",
                "redirect_to_kb": True  # signal for frontend to send next message to /kb/ask
            })

        # If unrecognized message
        return jsonify({
            "reply": "🤖 Sorry, I didn't understand that. Please choose an option or type *menu*."
        })

    except Exception as e:
        print("❌ Error in chat route:", e)
        return jsonify({"error": str(e)}), 500
