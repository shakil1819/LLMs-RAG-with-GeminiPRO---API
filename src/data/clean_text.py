import os

# Define the path to the text file
file_path = './merged.txt'

# Define the phrases to remove
phrases_to_remove = [
    "OK REJECT",
    "GET STARTED",
    "Our website use cookies to improve your experience.",
    "Skip to content",
    "Gigalogy Tutorial",
    "Overview",
    "Account and Project creation",
    "Credentials",
    "Personalizer",
    "MyGPT",
    "API Reference",
    "Release notes",
    "Glossary",
    "Table of contents",
    "Tutorial",
    "API Reference",
    "Overview"
]

# Read the file content
with open(file_path, 'r') as file:
    content = file.read()

# Remove the phrases from the content
for phrase in phrases_to_remove:
    content = content.replace(phrase, '')

# Write the updated content back to the file
with open(file_path, 'w') as file:
    file.write(content)

print(f"Phrases removed from {file_path}")