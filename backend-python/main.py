from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Route Blueprints
from routes.chat_routes import chat_bp
from routes.file_routes import file_bp
from routes.whatsapp_routes import whatsapp_bp
from routes.kb_routes import kb_bp  # ✅ Import Knowledge Base route

# Pinecone Initialization
from utils.pinecone_handler import initialize_pinecone

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize Pinecone
initialize_pinecone()

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(whatsapp_bp)  
# app.register_blueprint(kb_bp, url_prefix="/api/kb")  # ✅ Knowledge base API

@app.route("/")
def index():
    return {"message": "🚀 Python backend running for BetelBrio"}

if __name__ == "__main__":
    print("🚀 Flask server is starting...")
    app.run(debug=True, port=5000)
