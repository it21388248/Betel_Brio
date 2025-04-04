import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

index_name = "quickstart"
dimension = 1536

# ✅ Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def initialize_pinecone():
    try:
        existing_indexes = pc.list_indexes().names()
        if index_name not in existing_indexes:
            print(f"✅ Creating new index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
                )
            )
        else:
            print(f"✅ Using existing index: {index_name}")
    except Exception as e:
        print("❌ Error initializing Pinecone:", e)

def get_index():
    return pc.Index(index_name)

def upsert_to_pinecone(id, vector, text, filename, data_source):
    try:
        index = get_index()

        # Optional: chunk long documents into smaller pieces before upserting
        index.upsert(vectors=[{
            "id": id,
            "values": vector,
            "metadata": {
                "text": text[:1000],  # truncate long text
                "filename": filename,
                "dataSourceName": data_source
            }
        }])
        print(f"✅ Upserted vector for file '{filename}' with ID {id}")
    except Exception as e:
        print("❌ Error during upsert:", e)

def query_pinecone(vector, top_k=3):
    try:
        index = get_index()
        response = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )

        matches = response.get("matches", [])
        print(f"🔍 Pinecone matches found: {len(matches)}")
        for match in matches:
            score = match.get("score", 0)
            snippet = match.get("metadata", {}).get("text", "")[:100]
            print(f"→ Score: {score:.4f} | Snippet: {snippet}")

        if not matches:
            return None

        return "\n".join([m["metadata"]["text"] for m in matches if "metadata" in m])
    except Exception as e:
        print("❌ Error during query:", e)
        return None

def delete_from_pinecone(file_id):
    try:
        index = get_index()
        index.delete(ids=[file_id])
        print(f"🗑️ Deleted vector with ID: {file_id}")
    except Exception as e:
        print("❌ Error during delete:", e)
