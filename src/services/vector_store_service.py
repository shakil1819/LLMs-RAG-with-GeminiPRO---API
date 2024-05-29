import getpass
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
import qdrant_client
import nest_asyncio
import json
import warnings
from langchain.schema import Document
import re
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Step 1: Configurations (Gemini, QDrant)
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
warnings.filterwarnings("ignore")
nest_asyncio.apply()
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")

# Gemini AI vector Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Gemini AI model
llm = ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=gemini_api_key)

# Step 2: Dataset loading
docs_transformed = "../data/merged.txt"

# Step 3: Dataset Splitting and chunking
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=2048, 
    chunk_overlap=10
)

with open(docs_transformed, 'r') as f:
    text = f.read()

print('\n>Splitting documents into chunks')
chunks = splitter.split_text(text)

# Step 4: Create QDrant VectorDB setup (Cloud)
def qdrant_collection(text_chunks, embedding_model, collection_name):
    print("> Creating QdrantDB connection")
    
    # Create a Qdrant Client
    client = qdrant_client.QdrantClient(
        qdrant_url, 
        api_key=qdrant_api_key
    )
    print(">\nQdrant connection established.")
    
    # Create a collection
    vectors_config = qdrant_client.http.models.VectorParams(
        size=768,
        distance=qdrant_client.http.models.Distance.COSINE
    )
    
    # Let's create collection
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=vectors_config
    )
    
    # Create a list of Document objects
    documents = [Document(page_content=chunk) for chunk in text_chunks]
    
    # Save in Qdrant DB
    qdrant = Qdrant.from_documents(
        documents,
        embedding_model,
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True,
        collection_name=collection_name
    )
    print("> Chunk of text saved in Qdrant DB")

# Run the overall processing
print("VECTOR EMBEDDING PROCESS BEGINS")
docs = "../data/merged.txt"

qdrant_collection(chunks, embeddings, collection_name='rag-gemini')