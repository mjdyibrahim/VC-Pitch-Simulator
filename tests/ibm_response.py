from langchain_ibm.llms import WatsonxLLM
from app.config import IBM_API_KEY, IBM_CLOUD_URL, PROJECT_ID

def test_ibm_connection():
    # Initialize WatsonxAI client
    watsonx_ai = WatsonxLLM(
        api_key=IBM_API_KEY,
        service_url=IBM_CLOUD_URL,
        project_id=PROJECT_ID
    )

    # Sample text to send to IBM Granite
    sample_text = "Test connection with IBM Granite."

    # Call the IBM Granite function
    response = watsonx_ai.generate_text(
        model_id="granite-13b-chat-v2",
        inputs=[sample_text],
        parameters={
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 0,
            "stop_sequences": [],
            "repetition_penalty": 1
        },
        project_id=PROJECT_ID
    )

    # Print the response
    print("IBM Granite Response:", response)

if __name__ == "__main__":
    test_ibm_connection()
