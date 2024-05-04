# config/settings.py

import os

# Function to read secrets from files
def read_secret_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()

# Set paths to secret files
google_api_key_file = "/run/secrets/google_api_key"
qdrant_api_key_file = "/run/secrets/qdrant_api_key"
qdrant_url_file = "/run/secrets/qdrant_url"

# Read secrets from files
google_api_key = read_secret_file(google_api_key_file)
qdrant_api_key = read_secret_file(qdrant_api_key_file)
qdrant_url = read_secret_file(qdrant_url_file)

