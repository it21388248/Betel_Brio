from utils.predictor import predict_price, predict_demand_location
from utils.embeddings import get_embedding
from utils.pinecone_handler import query_pinecone
from openai import OpenAI
from collections import defaultdict
from utils.language_config import LANGUAGES
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
sessions = defaultdict(dict)

price_fields = ["Date", "Leaf_Type", "Leaf_Size", "Quality_Grade", "No_of_Leaves", "Location", "Season"]
demand_fields = ["Date", "No_of_Leaves", "Leaf_Type", "Leaf_Size", "Quality_Grade"]

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

    # Set language if not chosen
    if "lang" not in session:
        if message in ["1", "english"]:
            session["lang"] = "en"
            return LANGUAGES["en"]["greeting"]
        elif message in ["2", "සිංහල", "sinhala"]:
            session["lang"] = "si"
            return LANGUAGES["si"]["greeting"]
        elif message in ["3", "தமிழ்", "tamil"]:
            session["lang"] = "ta"
            return LANGUAGES["ta"]["greeting"]
        else:
            return (
                "🌐 Please select your language / කරුණාකර භාෂාව තෝරන්න / தயவுசெய்து உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்:\n\n"
                "1️⃣ English\n"
                "2️⃣ සිංහල\n"
                "3️⃣ தமிழ்"
            )

    lang = session["lang"]
    T = LANGUAGES[lang]

    if message == "menu":
        session.clear()
        return (
            "🌐 Please select your language / කරුණාකර භාෂාව තෝරන්න / தயவுசெய்து உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்:\n\n"
            "1️⃣ English\n"
            "2️⃣ සිංහල\n"
            "3️⃣ தமிழ்"
        )

    if message in ["hi", "hello", "hey"]:
        return T["greeting"]

    # ------------------ Option 1: Price Prediction ------------------
    if message in ["1", "start price prediction"] or session.get("collecting_price"):
        session["collecting_price"] = True
        session.setdefault("history", [])
        current_field = session.get("current_price_field")

        if message == "0":
            if session["history"]:
                prev_field = session["history"].pop()
                session.pop(prev_field, None)
                session["current_price_field"] = prev_field
                return T["price_questions"][prev_field]
            return "🔙 You're already at the beginning of the form."

        if current_field:
            if current_field in field_options and message.isdigit():
                index = int(message) - 1
                if 0 <= index < len(field_options[current_field]):
                    session[current_field] = field_options[current_field][index]
                    session["history"].append(current_field)
                else:
                    return T["invalid_option"].format(question=T["price_questions"][current_field])
            else:
                session[current_field] = message
                session["history"].append(current_field)

        for field in price_fields:
            if field not in session:
                session["current_price_field"] = field
                return T["price_questions"][field]

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
            return f"💰 Predicted price per leaf: *{predicted_price}*"
        except Exception as e:
            return f"⚠️ Error predicting price: {str(e)}"

    # ------------------ Option 2: Ask Question ------------------
    if message in ["2", "ask question", "question"]:
        return T["ask_question"]

    # ------------------ Option 3: Market Prediction ------------------
    if message in ["3", "market", "market info"] or session.get("collecting_market"):
        session["collecting_market"] = True
        session.setdefault("market", {})
        session.setdefault("market_history", [])
        market = session["market"]

        if not session.get("current_market_field") and "Date" not in market:
            session["current_market_field"] = demand_fields[0]
            return "📍 Let's find the most profitable market for your leaves!\n\n" + T["price_questions"][demand_fields[0]]

        current_field = session.get("current_market_field")

        if message == "0":
            if session["market_history"]:
                prev_field = session["market_history"].pop()
                market.pop(prev_field, None)
                session["current_market_field"] = prev_field
                return T["price_questions"][prev_field]
            else:
                return "🔙 You're already at the beginning of the form."

        if current_field:
            if current_field in field_options and message.isdigit():
                index = int(message) - 1
                if 0 <= index < len(field_options[current_field]):
                    market[current_field] = field_options[current_field][index]
                    session["market_history"].append(current_field)
                else:
                    return T["invalid_option"].format(question=T["price_questions"][current_field])
            else:
                market[current_field] = message
                session["market_history"].append(current_field)

        for field in demand_fields:
            if field not in market:
                session["current_market_field"] = field
                return T["price_questions"][field]

        try:
            best_location = predict_demand_location(
                market["Date"],
                int(market["No_of_Leaves"]),
                market["Leaf_Type"],
                market["Leaf_Size"],
                market["Quality_Grade"]
            )
            sessions.pop(session_id, None)
            return f"📍 Based on your data, the most profitable market is: *{best_location}*"
        except Exception as e:
            return f"⚠️ Error predicting market: {str(e)}"

    # ------------------ Fallback to Knowledge Base ------------------
    embedding = get_embedding(message)
    context = query_pinecone(embedding)
    if not context:
        return T["no_context"]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are BetelBrio, a smart assistant who helps users with betel predictions and answers based on uploaded documents."},
            {"role": "user", "content": f"Question: {message}\n\nContext: {context}"}
        ]
    )
    return response.choices[0].message.content
