from app.config import IBM_API_KEY, IBM_CLOUD_URL, PROJECT_ID
import requests

def call_ibm_granite(text):
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