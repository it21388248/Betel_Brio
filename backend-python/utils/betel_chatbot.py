from utils.predictor import predict_price
from utils.embeddings import get_embedding
from utils.pinecone_handler import query_pinecone
from openai import OpenAI
from collections import defaultdict
import os

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

def handle_message(message, session_id="default"):
    session = sessions[session_id]
    message = message.strip().lower()

    # Greeting with options
    if message in ["hi", "hello", "hey"]:
        sessions[session_id] = {}  # reset
        return "👋 Hello! I'm BetelBrio — your assistant for betel insights. Reply with:\n\n📈 *Start Price Prediction*\n💬 *Ask Question*"

    if message == "start price prediction" or session.get("collecting_price"):
        session["collecting_price"] = True
        current_field = session.get("current_price_field")
        if current_field:
            session[current_field] = message

        for field in price_fields:
            if field not in session:
                session["current_price_field"] = field
                return price_questions[field]

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
            sessions.pop(session_id, None)
            return f"💰 Predicted price per leaf: **{predicted_price}**"
        except Exception as e:
            return f"⚠️ Error predicting price: {str(e)}"

    if message == "ask question":
        return "🧠 Sure! Ask me anything related to betel farming or insights from the knowledge base."

    # Fallback: Ask Pinecone + OpenAI
    embedding = get_embedding(message)
    context = query_pinecone(embedding)
    if not context:
        return "⚠️ I can only answer based on the uploaded knowledge base or assist with predictions like price or demand."

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
    return response.choices[0].message.content
