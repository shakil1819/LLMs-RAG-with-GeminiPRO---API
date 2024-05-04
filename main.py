# main.py

from fastapi import FastAPI
from src.config.settings import gemini_api_key, qdrant_api_key, qdrant_url
from src.data.web_scraper import webscraper
from src.services.vector_store_service import create_qdrant_collection
from src.models.embeddings.embedding_model import setup_embeddings, setup_llm
from src.api.endpoints.question_answer import router as question_answer_router
from src.config.settings import gemini_api_key, qdrant_api_key, qdrant_url
from src.services.prompt_service import get_vector_store, get_prompt, process_llm_response
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(question_answer_router)
