import subprocess, requests
from fastapi import FastAPI
from src.api.endpoints.question_answer import router as question_answer_router
from PIL import Image
import streamlit as st

st.write("Hello Wordl")

# def fetch_data(input_text):
#     response = requests.post("http://backend:8000/ask", json={"input_text": input_text})
#     data = response.json()
#     return data
# # Define function to run Streamlit app
# def main():
#     st.set_page_config(page_title="RAG Assistant For Gigalogy")
#     st.markdown("# About Gigalogy :")
#     # image = Image.open('logo_horizontal.png')
#     # st.image(image, caption='by Shakil Mosharrof', use_column_width=True)
#     st.header("")
#     user_question = st.text_input("Type your question here")
#     if user_question:
#         # Call FastAPI endpoint to get response
#         # You can make an HTTP request to your FastAPI endpoint here
#         st.write("Response from FastAPI:")
#         st.write(f"{response}")
#         st.markdown("##### Source: ")
#         for source in sources: # Display source URLs
#             st.markdown(f"[{source}]({source})", unsafe_allow_html=True)

# # Start FastAPI server
# if __name__ == "__main__":
#     # Start Streamlit app in a separate subprocess
#     main()