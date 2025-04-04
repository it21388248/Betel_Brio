import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str):
    try:
        if not text or len(text.strip()) == 0:
            raise ValueError("Text is empty")

        trimmed = text[:4000]  # Avoid token overflow
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=trimmed
        )

        embedding = response.data[0].embedding
        print(f"📌 Embedding generated. Length: {len(embedding)}")
        return embedding

    except Exception as e:
        print("❌ Error generating embedding:", e)
        return None
