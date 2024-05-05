<h1 align="center">LLMs-RAG Implementation For Gigalogy Inc. Using Gemini Pro API, FastAPI & QDrant ( as vector DB)</h1>

---

![image](https://github.com/shakil1819/LLMs-RAG-with-GeminiPRO---API/assets/58840439/89256076-3ce2-4e7a-ac78-36fefcdf6d72)
<p align="center">
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
<img src="https://img.shields.io/badge/Google%20Generative%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/QDrant-FF6F61?style=for-the-badge&logo=qdrant&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>
<h2 align="center">RAG Assistant For Gigalogy</h2

---

## Tree of Directory
```CSS
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── main.py
├── requirements.txt
├── secrets
│   ├── google_api_key.secret
│   ├── qdrant_api_key.secret
│   └── qdrant_url.secret
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       └── question_answer.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── data
│   │   ├── __init__.py
│   │   └── web_scraper.py
│   ├── frontend
│   │   ├── __init__.py
│   │   ├── logo_horizontal.png
│   │   └── streamlit.py
│   ├── models
│   │   ├── __init__.py
│   │   └── embeddings
│   │       └── embedding_model.py
│   └── services
│       ├── __init__.py
│       ├── prompt_service.py
│       └── vector_store_service.py
└── tree.txt

10 directories, 25 files

```

## Description
This project is a Question-Answering Assistant on Gigalogy built using FastAPI and Streamlit. It uses the Google Generative AI (Gemini API) and Qdrant for document retrieval to provide accurate and relevant answers to user queries.

## Endpoints (FastAPI)
- `/ask`: 
    - **Method**: POST
    - **Input**: JSON {"question": "Your question here"}
    - **Output**: JSON {"answer": "Answer text", "sources": ["Source1", "Source2"]}

## Prerequisites
- Docker
- Docker Compose

## Installation and Run
1. Clone the repository:
    ```bash
    git clone https://github.com/shakil1819/LLMs-RAG-with-GeminiPRO---API.git
    ```
2. Navigate to the project directory:
    ```bash
    cd LLMs-RAG-with-GeminiPRO---API/
    ```
3. Run the following command to start the services:
    ```bash
    docker compose up --build
    ```
    ![gemnini](https://github.com/shakil1819/LLMs-RAG-with-GeminiPRO---API/assets/58840439/e49f73fc-080d-4c53-bee9-5fc24cc53d0e)

4. The backend will run on port `8000`, and the frontend (Streamlit app) will run on port `8501`.

## Configuration
- **Environment Variables**:
    - `GOOGLE_API_KEY`: API key for Google Generative AI.
    - `QDRANT_API_KEY`: API key for Qdrant.
    - `QDRANT_URL`: URL of the Qdrant service.
    - Follow this structure in order to achieve secrets via `docker-compose.yml`
        ```CSS
        ├── secrets
        │   ├── google_api_key.secret
        │   ├── qdrant_api_key.secret
        │   └── qdrant_url.secret
        ```

## Usage
1. Open your web browser and go to `http://localhost:8501` & `http://localhost:8000/docs` .
2. You will see a text box where you can type your question.
3. After entering your question and pressing Enter, the system will fetch and display the most relevant answer along with the source URLs.
