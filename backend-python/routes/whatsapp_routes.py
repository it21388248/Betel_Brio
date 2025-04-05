from flask import Blueprint, request
import requests
from utils.betel_chatbot import handle_message
import os

# ✅ Define the Blueprint first
whatsapp_bp = Blueprint("whatsapp", __name__)

# ✅ Environment variables
API_KEY = os.getenv("D360_API_KEY")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")  # e.g., https://waba.360dialog.io/v1/messages

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

        wa_from = "+" + data["contacts"][0]["wa_id"]
        user_msg = data["messages"][0]["text"]["body"]

        # 🧠 Handle message
        reply_text = handle_message(user_msg, session_id=wa_from)
        if not reply_text or not isinstance(reply_text, str):
            reply_text = "⚠️ Sorry, I couldn't process your request."

        # 📨 Send reply
        res = send_whatsapp_message(wa_from, reply_text)
        print("✅ Sent reply:", res.status_code, res.text)
        return "ok", 200

    except Exception as e:
        print("❌ Error in WhatsApp webhook:", str(e))
        return "error", 500
