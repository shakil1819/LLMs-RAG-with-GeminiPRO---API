import os
import sys
import time
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')