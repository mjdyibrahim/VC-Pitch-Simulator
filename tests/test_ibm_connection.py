from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_project_id = os.getenv("PROJECT_ID")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")

def test_ibm_connection(prompt):
    model = Model(
        model_id=ModelTypes.GRANITE_13B_CHAT_V2,
        params={
            GenParams.MAX_NEW_TOKENS: 900,
            GenParams.RETURN_OPTIONS: {
                'input_text': True,
                'generated_tokens': True,
            },
        },
        credentials=Credentials(
            api_key=ibm_api_key,
            url=ibm_cloud_url,
        ),
        project_id=ibm_project_id,
    )
    
    generated_response = model.generate(prompt=prompt)
    return generated_response

def parse_response(response):
    # Extract the generated text from the response
    generated_text = response.get('results', [{}])[0].get('generated_text', '')
    return generated_text

if __name__ == "__main__":
    prompt = "Hello, I need help with my startup today."
    response = test_ibm_connection(prompt)
    generated_text = parse_response(response)
    print("Generated Response:", generated_text)