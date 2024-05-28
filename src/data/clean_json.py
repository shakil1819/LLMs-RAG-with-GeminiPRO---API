import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the JSON data
json_file_path = os.path.join(script_dir, 'redoc.json')
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Define the output file path
output_file_path = os.path.join(script_dir, 'base_url_3.txt')

# Open the output text file
with open(output_file_path, 'w') as outfile:
    # Iterate over the endpoints
    for path, methods in data['paths'].items():
        for method, details in methods.items():
            # Write the endpoint and HTTP method
            outfile.write(f"Endpoint: {method}{path}\n")
            outfile.write(f"HTTP Method: {details['summary']}\n")
            
            # Check if description exists
            description = details.get('description', 'No description available.')
            outfile.write(f"Method Description: {description}\n")
            
            outfile.write("Responses:\n")
            
            # Write the response codes and descriptions
            for code, response in details['responses'].items():
                outfile.write(f" Code: {code} , Description: {response['description']}\n")
            
            outfile.write("Sample Request:\n")
            
            # Write the sample code snippets
            for sample in details.get('x-codeSamples', []):
                outfile.write(f" - Language: {sample['lang']}\n")
                outfile.write(f" - Code:\n{sample['source']}\n")
            
            outfile.write("\n--------------------------------\n")

print(f"Data has been successfully written to {output_file_path}")
