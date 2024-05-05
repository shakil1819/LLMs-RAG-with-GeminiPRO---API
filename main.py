# main.py

import subprocess
from fastapi import FastAPI
from src.api.endpoints.question_answer import router as question_answer_router
from src.frontend.streamlit import run_streamlit_app
from PIL import Image
import streamlit as st

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(question_answer_router)

# Run Streamlit app as a subprocess
subprocess.Popen(["streamlit", "run", "src/frontend/streamlit.py", "--server.address", "0.0.0.0", "--server.port", "8501"])


