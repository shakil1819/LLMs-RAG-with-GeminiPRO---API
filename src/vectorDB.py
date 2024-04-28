import getpass
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
import qdrant_client
import nest_asyncio
import json
import warnings
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
#===============END======================

#Step 2 : Dataset Pre processing and scraping
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

# Gemini AI vector Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Gemini AI model
llm = ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=gemini_api_key)


# Web Scrapping loader 
def webscrapper(urls: list):

    # load URLs
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()

    # Apply BS4 transformer
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
            # Extract content from given tags
            docs, tags_to_extract=["p", "h2", "span"]
        )
#===============END======================


# Step 3 : Dataset Splitting and chunking 

    # Perform Tokenization using Text Spliiter
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, 
        chunk_overlap=0)
    print('\n>Splitting documents into chunks')
    chunks = splitter.split_documents(docs_transformed)
    return chunks

#===============END======================


#Step 4 :  Create QDrant VectorDB setup (Cloud)

# Create Qdrant Collection to store vector embeddings
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
    
    # Save in Qdrant DB
    qdrant = Qdrant.from_documents(
        text_chunks,
        embedding_model,
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True,
        collection_name=collection_name
    )
    print("> Chunk of text saved in Qdrant DB")

#===============END======================


#===============Run the overall processing================
print("WEB SCRAPPING AND VECTOR EMBEDDING PROCESS BEGINS")
docs = webscrapper(URLs)

qdrant_collection(docs, embeddings, collection_name='rag-gemini')
#===============END======================
