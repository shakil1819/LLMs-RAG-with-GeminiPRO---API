FROM python:3.12.2

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501


CMD source /app/.venv/bin/activate && exec streamlit run app.py
# FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Streamlit
# CMD ["streamlit", "run", "main.py", "--server.port", "8501"]
# CMD ["streamlit", "run", "app.py"]
# ENTRYPOINT ["streamlit", "run"]
