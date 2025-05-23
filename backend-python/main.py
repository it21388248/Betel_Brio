from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Route Blueprints
from routes.chat_routes import chat_bp
from routes.file_routes import file_bp
from routes.whatsapp_routes import whatsapp_bp
from routes.kb_routes import kb_bp


# Pinecone Initialization
from utils.pinecone_handler import initialize_pinecone

# Airtable Integration (optional, use when needed)
from utils.airtable_service import save_report


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize Pinecone
initialize_pinecone()

# Register Blueprints
app.register_blueprint(chat_bp, url_prefix="/api/chat")
app.register_blueprint(file_bp, url_prefix="/api/files")
app.register_blueprint(whatsapp_bp)  
app.register_blueprint(kb_bp, url_prefix="/api/kb")



# 🧪 Optional test route to save a dummy report

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

if __name__ == "__main__":
    print("🚀 Flask server is starting...")
    app.run(debug=True, port=5000)
