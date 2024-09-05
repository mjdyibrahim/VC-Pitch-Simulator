import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ibm_api import initialize_watsonx_ai

def test_ibm_connection():
    # Initialize WatsonxAI client
    watsonx_ai = initialize_watsonx_ai()

    # Sample text to send to IBM Granite
    sample_text = "Test connection with IBM Granite."

    # Call the IBM Granite function
    response = watsonx_ai.generate_text(
        prompt=[sample_text],
    )

    # Print the response
    print("IBM Granite Response:", response)

if __name__ == "__main__":
    test_ibm_connection()
