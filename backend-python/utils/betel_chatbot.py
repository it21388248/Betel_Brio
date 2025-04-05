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
    "Leaf_Type": (
        "🌿 What is the leaf type?\n"
        "1️⃣ Peedichcha\n"
        "2️⃣ Korikan\n"
        "3️⃣ Keti\n"
        "4️⃣ Raan Keti"
    ),
    "Leaf_Size": (
        "📏 What is the leaf size?\n"
        "1️⃣ Small\n"
        "2️⃣ Medium\n"
        "3️⃣ Large"
    ),
    "Quality_Grade": (
        "✅ What is the quality grade?\n"
        "1️⃣ Ash\n"
        "2️⃣ Dark"
    ),
    "No_of_Leaves": "🍃 How many leaves do you have?",
    "Location": (
        "📍 What is your location?\n"
        "1️⃣ Kuliyapitiya\n"
        "2️⃣ Naiwala\n"
        "3️⃣ Apaladeniya"
    ),
    "Season": (
        "🗓️ What season is it?\n"
        "1️⃣ Dry\n"
        "2️⃣ Rainy"
    )
}

field_options = {
    "Leaf_Type": ["Peedichcha", "Korikan", "Keti", "Raan Keti"],
    "Leaf_Size": ["Small", "Medium", "Large"],
    "Quality_Grade": ["Ash", "Dark"],
    "Location": ["Kuliyapitiya", "Naiwala", "Apaladeniya"],
    "Season": ["Dry", "Rainy"]
}

def handle_message(message, session_id="default"):
    session = sessions[session_id]
    message = message.strip().lower()

    # Menu or greetings
    if message in ["hi", "hello", "hey", "menu"]:
        sessions[session_id] = {}  # reset session
        return (
            "👋 Hello! I'm *BetelBrio*, your assistant for betel insights.\n\n"
            "Please reply with:\n"
            "1️⃣ *Start Price Prediction*\n"
            "2️⃣ *Ask a Question*\n"
            "3️⃣ *Market Info (Coming Soon)*"
        )

    # Option 1 - Price Prediction
    if message in ["1", "start price prediction"] or session.get("collecting_price"):
        session["collecting_price"] = True
        current_field = session.get("current_price_field")
        if current_field:
            # Convert number option to actual value if valid
            if current_field in field_options and message.isdigit():
                index = int(message) - 1
                if 0 <= index < len(field_options[current_field]):
                    session[current_field] = field_options[current_field][index]
                else:
                    return f"❌ Invalid selection. Please choose a number:\n{price_questions[current_field]}"
            else:
                session[current_field] = message

        # Ask next field
        for field in price_fields:
            if field not in session:
                session["current_price_field"] = field
                return price_questions[field]

        # All fields collected – predict
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

    # Option 2 - Ask a Question
    if message in ["2", "ask question", "question"]:
        return "🧠 Sure! Ask me anything related to betel farming or insights from the knowledge base."

    # Option 3 - Market Info (Placeholder)
    if message in ["3", "market", "market info"]:
        return "📊 Market info is coming soon! Stay tuned."

    # Fallback – use knowledge base via Pinecone + OpenAI
    embedding = get_embedding(message)
    context = query_pinecone(embedding)
    if not context:
        return (
            "⚠️ I can only answer based on the uploaded knowledge base or assist with predictions like price or demand.\n\n"
            "Type *menu* to go back to main options."
        )

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
