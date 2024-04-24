from fastapi import FastAPI, HTTPException
from langchain_community.vectorstores import Qdrant
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import uvicorn
import textwrap
import qdrant_client
import streamlit as st
from PIL import Image
import multiprocessing

app = FastAPI()

# Step 1: Configurations [QDrant & Gemini]
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")

# Step 2: Define prompt [prompt engineering]
sys_prompt = """
    You are a helpful assistant to answer and guide for Gigalogy Company. Always answer as helpful and as relevant
    as possible, while being informative. Keep answer length about 100-200 words.
    
    If you don't know the answer to a question, please don't share false information.    
"""

instruction = """CONTEXT:\n\n {context}\n\nQuery: {question}\n"""

# Get vector store in action
def get_vector_store():
    # Connect to the QdrantDB Cloud
    client = qdrant_client.QdrantClient(
        qdrant_url,
        api_key=qdrant_api_key
    )
    
    # Define Embeddings 
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Vector store for Retrieval
    vector_store = Qdrant(
        client=client,
        collection_name='rag-gemini',
        embeddings=embeddings
    )
    
    return vector_store

# Format the prompt 
def get_prompt(instruction, sys_prompt):
    prompt_template =  sys_prompt + instruction
    return prompt_template

# Custom output parser
def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

# Return generated text and source in an output
def process_llm_response(llm_response):
    # Get parsed answer 
    text = wrap_text_preserve_newlines(llm_response['result'])
    
    # Uncouple metadata and return it
    sources=[]
    for source in llm_response["source_documents"]:
        sources.append(source.metadata['source'])
    return text, list(set(sources))

# Define vector store
vector_store = get_vector_store()

# Using Gemini-Pro 
llm = ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=gemini_api_key, temperature=0.9, max_tokens=1024, convert_system_message_to_human=True)

# Generate Prompt Template
prompt_template = get_prompt(instruction, sys_prompt)
QA_prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Create Retrieval Chain 
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vector_store.as_retriever(search_kwargs={"k":3}),
    return_source_documents=True, # Get source 
    chain_type_kwargs={"prompt":QA_prompt}
)

# @app.post("/ask")
# async def ask(question: str):
#     try:
#         llm_res = qa_chain.invoke(question)
#         response, sources = process_llm_response(llm_res)
#         return {"answer": response, "sources": sources}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

def run_streamlit_app():
    st.set_page_config(page_title="RAG Assistant For Gigalogy")
    
    st.markdown("# About Gigalogy :")
    
    image = Image.open('logo_horizontal.png')
    st.image(image, caption='by Shakil Mosharrof', use_column_width=True)

    st.header("")
    
    # Create text box so user can write query
    user_question = st.text_input("Type your question here")
    if user_question:
        llm_res = qa_chain.invoke(user_question) # Generate response
        response, sources = process_llm_response(llm_res) # Trim it using Output Parser
        st.write()
        st.write()
        st.markdown("### Based on your search:")
        st.write(f"{response}")
        st.markdown("##### Source: ")
        for source in sources: # Display source URLs
            st.markdown(f"[{source}]({source})", unsafe_allow_html=True)

if __name__ == "__main__":
    # Start Streamlit app in the main process
    run_streamlit_app()