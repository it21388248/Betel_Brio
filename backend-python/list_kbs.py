# list_kbs.py

from utils.pinecone_handler import get_index
import os
from dotenv import load_dotenv

load_dotenv()

def list_kbs_by_query():
    try:
        index = get_index()

        stats = index.describe_index_stats()
        total_vectors = stats.get("total_vector_count", 0)
        print(f"📦 Total vectors in Pinecone: {total_vectors}")

        if total_vectors == 0:
            print("📭 No knowledge base data found.")
            return

        # 🔍 Dummy vector (same dimension) to trigger top_k matches
        dummy_vector = [0.0] * 1536  # make sure this matches your `dimension`

        print("🔍 Querying to retrieve KB metadata...\n")

        response = index.query(
            vector=dummy_vector,
            top_k=100,
            include_metadata=True
        )

        for match in response.get("matches", []):
            metadata = match.get("metadata", {})
            vector_id = match.get("id", "N/A")
            filename = metadata.get("filename", "Unknown")
            source = metadata.get("dataSourceName", "Unknown")
            snippet = metadata.get("text", "")[:100]

            print(f"🧠 ID: {vector_id}")
            print(f"   📄 File: {filename}")
            print(f"   📁 Source: {source}")
            print(f"   📝 Snippet: {snippet}\n")

    except Exception as e:
        print("❌ Error fetching KBs:", e)

if __name__ == "__main__":
    list_kbs_by_query()
