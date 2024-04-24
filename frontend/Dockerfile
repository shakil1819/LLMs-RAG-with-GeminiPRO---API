FROM python:3.12.2

COPY requirements.txt app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit","run"]

CMD ["streamlit_app.py"]