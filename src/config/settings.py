# config/settings.py

import os

# Define paths to secret files
google_api_key_file = os.environ.get("GOOGLE_API_KEY_FILE")
qdrant_api_key_file = os.environ.get("QDRANT_API_KEY_FILE")
qdrant_url_file = os.environ.get("QDRANT_URL_FILE")

# Read API keys and URLs from secret files
def read_secret_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

# Retrieve API keys and URLs
google_api_key = read_secret_file(google_api_key_file)
qdrant_api_key = read_secret_file(qdrant_api_key_file)
qdrant_url = read_secret_file(qdrant_url_file)
