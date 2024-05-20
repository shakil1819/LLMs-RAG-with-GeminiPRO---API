# src/services/prompt_service.py

from langchain_community.vectorstores import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import qdrant_client
import textwrap
from src.config.settings import google_api_key,qdrant_api_key,qdrant_url
from src.data.web_scraper import all_chunks


# load_dotenv()
qdrant_api_key = qdrant_api_key
qdrant_url = qdrant_url

# Get vector store in action
def get_vector_store():
    # Connect to the QdrantDB Cloud
    client = qdrant_client.QdrantClient(
        qdrant_url,
        api_key=qdrant_api_key
    )
    
    # Define Embeddings 
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    
    # Vector store for Retrieval
    vector_store = Qdrant(
        client=client,
        collection_name='rag-gemini-new',
        embeddings=embeddings
    )
    
    return vector_store

# Format the prompt 
def get_prompt(instruction, sys_prompt):
    prompt_template =  sys_prompt + instruction
    return prompt_template

# Custom output parser
def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

# Return generated text and source in an output
def process_llm_response(llm_response):
    # Get parsed answer 
    text = wrap_text_preserve_newlines(llm_response['result'])
    
    # Uncouple metadata and return it
    sources=[]
    for source in llm_response["source_documents"]:
        sources.append(source.metadata['source'])
    return text, list(set(sources))
