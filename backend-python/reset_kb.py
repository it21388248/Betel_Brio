# reset_kb.py

from utils.pinecone_handler import get_index
import os
from dotenv import load_dotenv

load_dotenv()  # Load Pinecone API key and environment

def delete_all_vectors():
    try:
        index = get_index()
        index.delete(delete_all=True)
        print("🧹 All vectors deleted from Pinecone index.")
    except Exception as e:
        print("❌ Error deleting all vectors:", e)

if __name__ == "__main__":
    delete_all_vectors()
