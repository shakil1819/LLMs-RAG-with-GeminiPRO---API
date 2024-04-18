import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import os

def clean_text(text):#Dataset Cleaning
    # Remove redundant spaces and newline characters
    cleaned_text = re.sub('\s+', ' ', text).strip()
    return cleaned_text

def get_sitemap_urls(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            xml_content = response.content
            root = ET.fromstring(xml_content)
            urls = [elem.text for elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if '/ja' not in elem.text]
            return urls
        else:
            print(f"Failed to retrieve sitemap: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_page_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            cleaned_text = clean_text(text)
            return cleaned_text
        else:
            print(f"Failed to retrieve page: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

sitemap_url = "https://gigalogy.com/sitemap.xml"
urls = get_sitemap_urls(sitemap_url)

# Create a directory to store individual text files
if not os.path.exists('text_files'):
    os.makedirs('text_files')

# Write the texts to separate text files and merge them into one
merged_text = ""
for url in urls:
    text = get_page_text(url)
    if text:
        file_name = f"text_files/{url.split('/')[-2]}.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n")
            file.write(f"Text: {text}\n")
            file.write("-" * 50 + "\n")
        
        # Add to merged text
        merged_text += f"URL: {url}\n"
        merged_text += f"Text: {text}\n"
        merged_text += "-" * 50 + "\n"

# Write the merged text to info.txt
with open('info.txt', 'w', encoding='utf-8') as file:
    file.write(merged_text)

print("Information written to info.txt and individual text files.")