from qdrant_client.models import PointStruct, VectorParams, Distance
import google.generativeai as gemini_client
import os
import qdrant_client
from dotenv import load_dotenv

# Load environment variables from .env file

gemini_api_key = "AIzaSyCB7mG7dX3qrv2SUrZZ-5f5pJ6GZpleKlw"
qdrant_api_key = "UNImexEbR-mV-Ous_gqQPul7Lb01Qxa9fG_O0jnN5vFmGe0uBgnZzg"
qdrant_url = "https://f2d1c961-076f-4551-b1f9-61a19a649108.us-east4-0.gcp.cloud.qdrant.io:6333"
def add_documents_to_collection(collection_name, qdrant_client, chunk_size=2048, overlap=100):
    try:
        # Get the path to the directory containing this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define the path to the scraped_data folder within the same directory
        text_files_dir = os.path.join(script_dir, "scraped_data")

        # Read all the .txt files from the text_files folder
        documents = []
        for filename in os.listdir(text_files_dir):
            if filename.endswith(".txt" and ".json"):
                file_path = os.path.join(text_files_dir, filename)
                with open(file_path, "r") as file:
                    document = file.read()
                    documents.append(document)
                    
        # Remove any leading or trailing whitespace from the lines
        documents = [doc.strip() for doc in documents]


        # Chunk and overlap the documents
        chunked_documents = []
        for doc in documents:
            for i in range(0, len(doc), chunk_size - overlap):
                chunk = doc[i:i + chunk_size]
                chunked_documents.append(chunk)

        # Embed documents using gemini_client
        results = [
            gemini_client.embed_content(
                model="models/embedding-001",
                content=document,
                task_type="retrieval_document",
                title="Qdrant x Gemini",
            )
            for document in chunked_documents
        ]

        # Creating Qdrant Points
        points = [
            PointStruct(
                id=idx,
                vector=response["embedding"],
                payload={"text": document},
            )
            for idx, (response, document) in enumerate(zip(results, chunked_documents))
        ]
        from config.settings import qdrant_client 
        # Create Collection
        qdrant_client.create_collection(
            collection_name="test",
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE,
            ),
        )

        # Add to Collection
        qdrant_client.upsert(collection_name, points)
        print("Documents added successfully to the collection.")
    except Exception as e:
        print(f"An error occurred while setting up qdrant collection: {e}")