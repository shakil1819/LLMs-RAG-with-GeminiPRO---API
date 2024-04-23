import os
import sys
import time
import pathlib
import textwrap
import google.generativeai as genai
import google.ai.generativelanguage as glm
from IPython.display import display
from IPython.display import Markdown
from dotenv import load_dotenv
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionStatus
from qdrant_client.models import PointStruct
from qdrant_client.models import Distance, PointStruct, VectorParams
from lucknowllm import UnstructuredDataLoader, split_into_segments
import numpy as np

load_dotenv()

#Step 1:  Initialize Gemini API Key and Select Models
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-pro')

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Step 2: Initialize Qdrant Client
client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="rag",
    vectors_config=models.VectorParams(size=4, distance=models.Distance.COSINE),
)

# Step 3: Load Dataset
loader = TextLoader("./info.txt")
loader.load()

# Step 4: Split Dataset (Tokenization)
with open("./info.txt") as f:
    info = f.read()
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1024,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([info])

# Step 5 : Create Embeddings
embeddings = []
for sentence in texts:
    embedding_response = genai.embed_content(
        model="models/embedding-001",
        content=sentence,
        task_type="retrieval_document", 
        title="Qdrant x Gemini",
    )
    embeddings.append(embedding_response.embedding)

# Create Qdrant Vector Store
vector_store = Qdrant(
    client=client,
    collection_name="rag",
    vector_dim=4,  # adjust the vector dimension according to your needs
)

# Create LangChain Index
index = VectorStoreIndex(nodes=texts, storage_context=vector_store)

# Create Gemini Model
gemini_model = setup_gemini_model("gemini-pro", os.getenv('API_KEY'), 0.7)

# Create RAG QA Chain
qa_chain = create_rag_qa_chain(gemini_model, index)

def setup_gemini_model(model_name, api_key, temperature):
    """Sets up a Gemini model."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    generation_config = {
        "temperature": temperature,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [...]  # define your safety settings here
    return model

def create_rag_qa_chain(model, vector_index):
    """Creates a Retrieval-Augmented Generation QA chain."""
    return RetrievalQA(model, vector_index)