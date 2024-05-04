# src/services/vector_store_service.py

import qdrant_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Qdrant
from src.config.settings import google_api_key,qdrant_api_key,qdrant_url



def create_qdrant_collection(text_chunks, embedding_model, collection_name, qdrant_url, qdrant_api_key):
    print("> Creating QdrantDB connection")
    
    # Create a Qdrant Client
    client = qdrant_client.QdrantClient(qdrant_url, api_key=qdrant_api_key)
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
