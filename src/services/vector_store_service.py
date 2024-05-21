# src/services/vector_store_service.py

import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from src.data.web_scraper import all_chunks
from src.config.settings import google_api_key, qdrant_api_key, qdrant_url

# src/services/vector_store_service.py
collection_name = "rag-gemini-21052024"
gemini_api_key = google_api_key  # Assuming google_api_key is set in settings
# src/services/vector_store_service.py

def create_qdrant_collection(text_chunks, gemini_api_key, collection_name, qdrant_url, qdrant_api_key):
    print("> Creating QdrantDB connection")
    
    # Create a Qdrant Client
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    print(">\nQdrant connection established.")
    
    # Configure Gemini client
    gemini_client.configure(api_key=gemini_api_key)
    
    # Generate embeddings for text chunks using Gemini
    embeddings = []
    for chunk in text_chunks:
        response = gemini_client.embed_content(
            model="models/embedding-001",
            content=chunk,
            task_type="retrieval_document",
            title="Document Chunk"
        )
        embeddings.append(response['embedding'])
    
    # Create points for upserting into Qdrant
    points = [
        PointStruct(
            id=idx,
            vector=embedding,
            payload={"text": chunk}
        )
        for idx, (chunk, embedding) in enumerate(zip(text_chunks, embeddings))
    ]
    
    # Create collection in Qdrant
    vectors_config = VectorParams(
        size=768,  # Assuming the Gemini embedding size is 768
        distance=Distance.COSINE
    )
    
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=vectors_config
    )
    
    # Upsert points into Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("> Chunks of text saved in Qdrant DB")

# Parameters


# Execute the function
create_qdrant_collection(
    text_chunks=[chunk for sublist in all_chunks for chunk in sublist],  # Flatten the list of chunks
    gemini_api_key=gemini_api_key,
    collection_name=collection_name,
    qdrant_url=qdrant_url,
    qdrant_api_key=qdrant_api_key
)