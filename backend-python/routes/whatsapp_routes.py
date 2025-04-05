from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from utils.betel_chatbot import handle_message

whatsapp_bp = Blueprint("whatsapp", __name__)

@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "default")  # use sender's WhatsApp number as session_id

    print(f"📨 WhatsApp: {incoming_msg} from {sender}")

    reply = handle_message(incoming_msg, session_id=sender)

    response = MessagingResponse()
    response.message(reply)
    return str(response)
