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

# Define vector store
vector_store = get_vector_store()

# Using Gemini-Pro 
llm = ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=gemini_api_key, temperature=0.9, max_tokens=1024, convert_system_message_to_human=True)

# Load URLs for web scraping
URLs = ['https://gigalogy.com/',
        'https://gigalogy.com/personalization-platform/',
        'https://gigalogy.com/personalization-use-case/',
        'https://gigalogy.com/gpt-flow-platform/',
        'https://gigalogy.com/gcore-platform/',
        'https://gigalogy.com/smartads-platform/',
        'https://gigalogy.com/smartads-use-case/',
        'https://gigalogy.com/about-us/',
        'https://gigalogy.com/mission/',
        'https://www.gigalogy.com/team/',
        'https://gigalogy.com/career/',
        'https://gigalogy.com/developer-program/',
        'https://gigalogy.com/request-demo/',
        'https://gigalogy.com/event/',
        'https://gigalogy.com/press-room/',
        'https://gigalogy.com/developer/',
        'https://platform.gigalogy.com/solutions'
]

# Define routes
@app.get("/")
async def run_processing():
    # Step 1: Setup embeddings and LLM
    embeddings = setup_embeddings()
    llm = setup_llm(gemini_api_key)

    # Step 2: Web scraping
    docs = await webscraper(URLs)

    # Step 3: Create QDrant collection
    create_qdrant_collection(docs, embeddings, collection_name='rag-gemini', qdrant_url=qdrant_url, qdrant_api_key=qdrant_api_key)

    return {"message": "Processing complete!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

