##########1.Import Libraries##############
import os
import sys
import time
import pathlib
import textwrap
import google.generativeai as genai
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
from qdrant_client.models import Distance, VectorParams
import numpy as np

#from sentence_transformers import SentenceTransformer : to import hugging face hub models
from tqdm.notebook import tqdm
load_dotenv()
##########END IMPORT####################

##########2.Initialize Gemini API Key, Select Models#############
genai.configure(api_key=os.getenv('API_KEY'))
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat
#--------------------------------------------------------------

##########3.Initialize Qdrant Client#############
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="rag",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)

##############3. loading the dataset ##########
loader = TextLoader("./info.txt")
loader.load()
#print(loader)


########### 4. Splitting Dataset #############
with open("./info.txt") as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1024,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])