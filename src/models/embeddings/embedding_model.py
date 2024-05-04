# src/models/embeddings/embedding_model.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.settings import google_api_key,qdrant_api_key,qdrant_url

with open("/run/secrets/google_api_key", "r") as google_api_key_file:
    google_api_key = google_api_key_file.read().strip()

with open("/run/secrets/qdrant_api_key", "r") as qdrant_api_key_file:
    qdrant_api_key = qdrant_api_key_file.read().strip()

with open("/run/secrets/qdrant_url", "r") as qdrant_url_file:
    qdrant_url = qdrant_url_file.read().strip()

def setup_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def setup_llm(gemini_api_key):
    return ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=google_api_key)
