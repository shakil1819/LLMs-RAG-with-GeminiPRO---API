# main.py

from fastapi import FastAPI
from src.api.endpoints.question_answer import router as question_answer_router


# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(question_answer_router)
