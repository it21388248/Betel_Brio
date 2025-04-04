import os
import uuid
from datetime import datetime  # ✅ Added for correct timestamp
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from utils.text_extractor import extract_text
from utils.embeddings import get_embedding
from utils.pinecone_handler import upsert_to_pinecone, delete_from_pinecone
from utils.file_db import load_files, save_files

file_bp = Blueprint("files", __name__)
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
uploaded_files = load_files()  # ✅ Load file metadata from JSON


@file_bp.route("/upload", methods=["POST"])
def upload():
    try:
        from utils.chunker import split_text_into_chunks  # ✅ Import inside to avoid circular import
        file = request.files["file"]
        data_source = request.form.get("dataSourceName", "Unknown")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)

        print(f"📥 Saved file: {filename}")
        text = extract_text(filepath)
        if not text:
            return jsonify({"error": "Text extraction failed"}), 400

        print(f"📄 Extracted text length: {len(text)}")

        # ✅ Split text into chunks for better vector matching
        chunks = split_text_into_chunks(text)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_id}_{i}"
            embedding = get_embedding(chunk)
            if not embedding:
                continue
            upsert_to_pinecone(chunk_id, embedding, chunk, filename, data_source)

        file_entry = {
            "id": file_id,
            "filename": filename,
            "timestamp": datetime.utcnow().isoformat(),
            "dataSourceName": data_source
        }
        uploaded_files.append(file_entry)
        save_files(uploaded_files)

        return jsonify({"message": "File uploaded and indexed", "id": file_id})
    except Exception as e:
        print("❌ Upload error:", e)
        return jsonify({"error": str(e)}), 500

    try:
        file = request.files["file"]
        data_source = request.form.get("dataSourceName", "Unknown")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)

        text = extract_text(filepath)
        if not text:
            return jsonify({"error": "Text extraction failed"}), 400

        embedding = get_embedding(text)
        upsert_to_pinecone(file_id, embedding, text, filename, data_source)

        file_entry = {
            "id": file_id,
            "filename": filename,
            "timestamp": datetime.utcnow().isoformat(),  # ✅ Correct date format
            "dataSourceName": data_source
        }
        uploaded_files.append(file_entry)
        save_files(uploaded_files)

        return jsonify({"message": "File uploaded and indexed", "id": file_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@file_bp.route("/list", methods=["GET"])
def list_files():
    return jsonify({"files": uploaded_files})


@file_bp.route("/delete/<file_id>", methods=["DELETE"])
def delete_file(file_id):
    try:
        file_entry = next((f for f in uploaded_files if f["id"] == file_id), None)
        if not file_entry:
            return jsonify({"error": "File not found"}), 404

        filepath = os.path.join(UPLOAD_DIR, file_entry["filename"])
        if os.path.exists(filepath):
            os.remove(filepath)

        delete_from_pinecone(file_id)
        uploaded_files.remove(file_entry)
        save_files(uploaded_files)

        return jsonify({"message": f"File {file_id} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
