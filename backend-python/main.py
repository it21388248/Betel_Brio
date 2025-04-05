from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.chat_routes import chat_bp
from routes.file_routes import file_bp
from routes.whatsapp_routes import whatsapp_bp  # ✅ Import WhatsApp route
from utils.pinecone_handler import initialize_pinecone

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

initialize_pinecone()

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(whatsapp_bp)   # ✅ Register WhatsApp route

@app.route("/")
def index():
    return {"message": "Python backend running 🐍"}

if __name__ == "__main__":
    print("🚀 Flask server is starting...")
    app.run(debug=True, port=5000)
