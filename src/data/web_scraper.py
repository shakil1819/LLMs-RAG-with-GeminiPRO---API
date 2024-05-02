# src/data/web_scraper.py

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

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
