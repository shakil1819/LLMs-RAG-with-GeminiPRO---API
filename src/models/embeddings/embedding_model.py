# src/models/embeddings/embedding_model.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def setup_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def setup_llm(gemini_api_key):
    return ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=gemini_api_key)
