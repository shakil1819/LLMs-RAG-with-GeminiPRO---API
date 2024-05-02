# src/data/web_scraper.py

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def webscraper(urls: list):
    # Load URLs
    loader = AsyncChromiumLoader(urls)
    docs = await loader.load()

    # Apply BS4 transformer
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p", "h2", "span"]
    )

    # Perform Tokenization using Text Splitter
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=3000, chunk_overlap=0
    )
    print('\n> Splitting documents into chunks')
    chunks = splitter.split_documents(docs_transformed)
    return chunks
