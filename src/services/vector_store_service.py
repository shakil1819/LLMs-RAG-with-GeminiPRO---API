import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from src.data.web_scraper import all_chunks
from src.config.settings import google_api_key, qdrant_api_key, qdrant_url
from itertools import chain

# Set the API keys and URL
gemini_api_key = "AIzaSyCB7mG7dX3qrv2SUrZZ-5f5pJ6GZpleKlw"
qdrant_api_key = "UNImexEbR-mV-Ous_gqQPul7Lb01Qxa9fG_O0jnN5vFmGe0uBgnZzg"
qdrant_url = "https://f2d1c961-076f-4551-b1f9-61a19a649108.us-east4-0.gcp.cloud.qdrant.io:6333"

# Collection name
collection_name = "rag-gemini-21052024"

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
    
    # Flatten the list of chunks
    text_chunks = list(chain.from_iterable(all_chunks))
    
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
    
    # Check if the collection already exists, and recreate it if necessary
    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=vectors_config
    )
    
    # Upsert points into Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    print("> Chunks of text saved in Qdrant DB")

# Execute the function
create_qdrant_collection(
    text_chunks=text_chunks,
    gemini_api_key=gemini_api_key,
    collection_name=collection_name,
    qdrant_url=qdrant_url,
    qdrant_api_key=qdrant_api_key
)