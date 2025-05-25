from flask import Flask
from flask import send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Route Blueprints
from routes.chat_routes import chat_bp
from routes.file_routes import file_bp
from routes.whatsapp_routes import whatsapp_bp
from routes.kb_routes import kb_bp

# Pinecone Initialization
from utils.pinecone_handler import initialize_pinecone

# Airtable Integration (optional, use when needed)
from utils.airtable_service import save_report

# Load .env
load_dotenv()

app = Flask(__name__)

# CORS config for Vercel frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


# Initialize Pinecone
initialize_pinecone()

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(whatsapp_bp)
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
app.register_blueprint(kb_bp, url_prefix="/api/kb")

@app.route('/api/files/list')

# Test Route
@app.route("/api/test-save-report")
def test_save_report():
    query = "Sample Query"
    response = "Sample Response"
    prediction = 0.85
    result = save_report(query, response, prediction)
    return {"message": "Report saved to Airtable", "record": result}

@app.route("/")
def index():
    return {"message": "🚀 Python backend running for BetelBrio"}

# ✅ Railway-compatible app startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
