from flask import Blueprint, request
import requests
from utils.betel_chatbot import handle_message
import os

# ✅ Define the Blueprint first
whatsapp_bp = Blueprint("whatsapp", __name__)

# ✅ Environment variables
API_KEY = os.getenv("D360_API_KEY")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")  # e.g., https://waba.360dialog.io/v1/messages

# ✅ Simple session tracking for message IDs
temp_sessions = {}

def send_whatsapp_message(recipient_id, message_text):
    headers = {
        "D360-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "to": recipient_id,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    print(f"Sent message to {recipient_id}, status: {response.status_code}")
    print("Response:", response.json())
    return response

@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        data = request.get_json()
        print("📨 Incoming:", data)

        if "messages" not in data or not data["messages"]:
            return "skipped - no message", 200

        message_obj = data["messages"][0]

        # ✅ Ignore non-text or non-user messages
        if message_obj.get("type") != "text" or "text" not in message_obj:
            return "ignored - not a user text", 200

        wa_from = "+" + data["contacts"][0]["wa_id"]
        user_msg = message_obj["text"]["body"]
        message_id = message_obj.get("id")

        # ✅ Ignore duplicate message
        if temp_sessions.get(wa_from) == message_id:
            print("🔁 Duplicate message ignored")
            return "duplicate", 200
        temp_sessions[wa_from] = message_id

        # 🧠 Handle message
        response_data = handle_message(user_msg, session_id=wa_from)
        if isinstance(response_data, str):
            reply_text = response_data
        elif isinstance(response_data, dict):
            reply_text = response_data.get("reply", "⚠️ Sorry, I couldn't process your request.")
            if response_data.get("redirect_to_kb"):
                kb_response = requests.post("http://localhost:5000/api/kb/ask", json={"message": user_msg}).json()
                reply_text = kb_response.get("reply", "⚠️ KB error.")
        else:
            reply_text = "⚠️ Unrecognized response format."

        # 📨 Send reply
        res = send_whatsapp_message(wa_from, reply_text)
        print("✅ Sent reply:", res.status_code, res.text)
        return "ok", 200

    except Exception as e:
        print("❌ Error in WhatsApp webhook:", str(e))
        return "error", 500