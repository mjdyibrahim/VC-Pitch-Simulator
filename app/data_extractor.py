import json
import getpass

IBM_API_KEY = os.getenv("IBM_API_KEY") or getpass.getpass("Please enter your WML api key (hit enter): ")
IBM_CLOUD_URL = os.getenv("IBM_CLOUD_URL", "https://us-south.ml.cloud.ibm.com")

try:
    PROJECT_ID = os.environ["PROJECT_ID"]
except KeyError:
    PROJECT_ID = input("Please enter your project_id (hit enter): ")
import os
print(f"Debug: Environment Variables - IBM_API_KEY: {os.getenv('IBM_API_KEY')}, IBM_CLOUD_URL: {os.getenv('IBM_CLOUD_URL')}, PROJECT_ID: {os.getenv('PROJECT_ID')}")
import requests

def call_ibm_granite(text):
    print(f"Debug: IBM_API_KEY starts with {IBM_API_KEY[:5]}")  # Debug statement
    headers = {
        "Authorization": f"Bearer {IBM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model_id": "granite-13b-chat-v2",
        "inputs": [text],
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID
    }
    
    response = requests.post(f"{IBM_CLOUD_URL}/ml/v1-beta/generation/text", headers=headers, json=data)
    return response.json()

def extract_data(text_content):
    # Use the IBM Granite model to extract data
    response = call_ibm_granite(text_content)
    
    # Process the response to extract relevant data
    # This is a placeholder; you'll need to implement the actual data extraction logic
    extracted_data = {
        "company_name": "Example Company",
        "industry": "Technology",
        "funding_stage": "Series A",
        # Add more fields as needed
    }
    
    return extracted_data
import os
import requests
from .config import IBM_API_KEY, IBM_CLOUD_URL, PROJECT_ID

def extract_data(text_content):
    # Load the predefined JSON template
    with open("data/startup_profile.json", "r") as file:
        prompt_template = json.load(file)

    # Format the prompt with the text content
    try:
        prompt = prompt_template["prompt"].format(text_content=text_content)
    except KeyError:
        raise KeyError("The key 'prompt' is missing from the JSON template.")

    # Prepare the request payload
    data = {
        "model_id": "granite-13b-chat-v2",
        "inputs": [prompt],
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        "project_id": PROJECT_ID
    }

    # Set the headers for the request
    headers = {
        "Authorization": f"Bearer {IBM_API_KEY}",
        "Content-Type": "application/json"
    }

    # Send the request to IBM Watson
    response = requests.post(f"{IBM_CLOUD_URL}/ml/v1-beta/generation/text", headers=headers, json=data)

    # Return the extracted data
    return response.json()
