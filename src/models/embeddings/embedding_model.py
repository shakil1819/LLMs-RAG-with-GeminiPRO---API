# src/models/embeddings/embedding_model.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.settings import google_api_key,qdrant_api_key,qdrant_url



def setup_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def setup_llm(google_api_key):
    return ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
