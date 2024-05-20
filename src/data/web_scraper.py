# src/data/web_scraper.py

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import os
from typing import List, Set

# Set to keep track of visited URLs to avoid duplicates for each base URL
visited_urls: Set[str] = set()

async def scrape_page(page, url: str) -> str:
    await page.goto(url)
    # Extract and write text content of the page
    text_content = await page.evaluate("document.body.innerText")
    return text_content

async def scrape_website(base_url: str, file_name: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        global visited_urls
        visited_urls = set()  # Reset visited URLs for each base URL
        
        text_content = await scrape_page(page, base_url)
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"URL: {base_url}\n")
            file.write(text_content)
            file.write("\n" + "="*80 + "\n")

        await browser.close()

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
# (Note: This part of the code is moved outside the web scraper as it requires the scraped data)



def load_and_split_documents(file_path: str) -> List[str]:
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, chunk_overlap=0
    )
    print('\n> Splitting documents into chunks')
    chunks = splitter.split_documents(documents)
    return chunks

# Assuming you have saved the scraped text files, use this part of the code to tokenize
file_path = "path/to/scraped_file.txt"
chunks = load_and_split_documents(file_path)