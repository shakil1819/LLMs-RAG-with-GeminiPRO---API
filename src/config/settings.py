#==This file contains Gemini, QDrant setup instructions===
# src/config/settings.py

import os
from dotenv import load_dotenv
import warnings
# import nest_asyncio

# Load environment variables
load_dotenv()

# Filter warnings
warnings.filterwarnings("ignore")

# Apply nest_asyncio
# nest_asyncio.apply()

# Retrieve API keys and URLs
gemini_api_key = os.getenv("GOOGLE_API_KEY")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
