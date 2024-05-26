from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, RecursiveJsonSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import os
from typing import List, Set
import json
from pathlib import Path
from pprint import pprint
import ujson
import fasttext

# Set to keep track of visited URLs to avoid duplicates for each base URL
visited_urls = set()

async def scrape_page(page, url, file):
    await page.goto(url)
    # Extract and write text content of the page
    text_content = await page.evaluate("document.body.innerText")
    file.write(f"URL: {url}\n")
    file.write(text_content)
    file.write("\n" + "="*80 + "\n")
    
    # Extract all links from the page
    links = await page.evaluate('''() => Array.from(document.querySelectorAll('a'))
                                  .map(a => a.href).filter(href => href.startsWith(location.origin) || !href.startsWith('http'))''')
    return links

async def scrape_website(base_url, file_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        global visited_urls
        visited_urls = set()  # Reset visited URLs for each base URL
        with open(file_name, 'w', encoding='utf-8') as file:
            await recursive_scrape(page, base_url, file, base_url)
        await browser.close()

async def recursive_scrape(page, url, file, base_url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    print(f"Scraping: {url}")
    links = await scrape_page(page, url, file)
    for link in links:
        # Resolve relative links
        absolute_link = urljoin(url, link)
        if urlparse(absolute_link).netloc == urlparse(base_url).netloc:
            await recursive_scrape(page, absolute_link, file, base_url)

# List of base URLs and corresponding output files
base_urls = {
    "http://gigalogy.com/": "base_url_1.txt",
    "https://tutorial.gigalogy.com/": "base_url_2.txt",
    "https://api.recommender.gigalogy.com/redoc": "base_url_3.txt"
}
# Run the async function for each base URL
async def main():
    for base_url, file_name in base_urls.items():
        print(f"Starting scraping for {base_url}")
        await scrape_website(base_url, file_name)

# Start the script
asyncio.run(main())

# Perform Tokenization using Text Splitter
def load_and_split_documents(file_paths: List[str], max_chunk_size=9000) -> List[List[str]]:
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=2048, chunk_overlap=100
    )
    print('\n> Splitting documents into chunks')
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        chunks = splitter.split_text(content)
        
        # Further split chunks if they exceed the max_chunk_size
        small_chunks = []
        for chunk in chunks:
            if len(chunk) > max_chunk_size:
                for i in range(0, len(chunk), max_chunk_size):
                    small_chunks.append(chunk[i:i + max_chunk_size])
            else:
                small_chunks.append(chunk)
        all_chunks.append(small_chunks)
    return all_chunks

# Assuming you have saved the scraped text files, use this part of the code to tokenize
file_paths = [
    "./base_url_1.txt",
    "./base_url_2.txt",
    "./base_url_3.txt"
]
all_chunks = load_and_split_documents(file_paths)
print('\n> Chunking and splitting completed.')

# Recursively split JSON
file_path = "./redoc.json"
json_splitter = RecursiveJsonSplitter(max_chunk_size=300)
json_data = ujson.loads(Path(file_path).read_text())
json_chunks = json_splitter.split_json(json_data=json_data)
print(f"\n> JSON chunks: {len(json_chunks)}")

import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
# from src.data.web_scraper import all_chunks
# from src.config.settings import google_api_key, qdrant_api_key, qdrant_url
from itertools import chain
import numpy as np

# gemini_api_key = "AIzaSyCB7mG7dX3qrv2SUrZZ-5f5pJ6GZpleKlw"
# qdrant_api_key = "UNImexEbR-mV-Ous_gqQPul7Lb01Qxa9fG_O0jnN5vFmGe0uBgnZzg"
# qdrant_url = "https://f2d1c961-076f-4551-b1f9-61a19a649108.us-east4-0.gcp.cloud.qdrant.io:6333"

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
        embeddings.append(np.array(response['embedding']))
    
    # Flatten the list of chunks
    text_chunk = list(chain.from_iterable(all_chunks))
    
    # Create points for upserting into Qdrant
    points = [
        PointStruct(
            id=idx,
            vector=embedding.tolist(),
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
    text_chunks=all_chunks,
    gemini_api_key=gemini_api_key,
    collection_name=collection_name,
    qdrant_url=qdrant_url,
    qdrant_api_key=qdrant_api_key
)