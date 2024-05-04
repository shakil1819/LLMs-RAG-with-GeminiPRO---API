# src/api/endpoints/question_answer.py
import os
from fastapi import APIRouter, HTTPException
from src.services.prompt_service import get_vector_store, get_prompt, process_llm_response
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

router = APIRouter()

# Step 1: Define vector store
vector_store = get_vector_store()

# Using Gemini-Pro 
llm = ChatGoogleGenerativeAI(model="gemini-pro", gemini_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.9, max_tokens=1024, convert_system_message_to_human=True)

# Generate Prompt Template
sys_prompt = """
    You are a helpful assistant to answer and guide for Gigalogy Company. Always answer as helpful and as relevant
    as possible, while being informative. Keep answer length about 100-200 words.
    
    If you don't know the answer to a question, please don't share false information.    
"""
instruction = """CONTEXT:\n\n {context}\n\nQuery: {question}\n"""
prompt_template = get_prompt(instruction, sys_prompt)
QA_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Create Retrieval Chain 
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", 
    retriever=vector_store.as_retriever(search_kwargs={"k":3}),
    return_source_documents=True, # Get source 
    chain_type_kwargs={"prompt":QA_prompt}
)

@router.post("/ask")
async def ask(question: str):
    try:
        llm_res = qa_chain.invoke(question)
        response, sources = process_llm_response(llm_res)
        return {"answer": response, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))