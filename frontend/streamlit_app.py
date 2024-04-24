import streamlit as st
from PIL import Image
import multiprocessing
import requests

def run_streamlit_app():
    st.set_page_config(page_title="RAG Assistant For Gigalogy")
    
    st.markdown("# About Gigalogy :")
    
    image = Image.open('logo_horizontal.png')
    st.image(image, caption='by Shakil Mosharrof', use_column_width=True)

    st.header("")
    
    # Create text box so user can write query
    user_question = st.text_input("Type your question here")
    
    if user_question:
        response = requests.post("http://backend:8000/ask", json={"question": user_question})
        data = response.json()
        
        st.write()
        st.write()
        st.markdown("### Based on your search:")
        st.write(f"{data['answer']}")
        st.markdown("##### Source: ")
        for source in data['sources']: # Display source URLs
            st.markdown(f"[{source}]({source})", unsafe_allow_html=True)

if __name__ == "__main__":
    run_streamlit_app()
