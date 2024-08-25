from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_project_id = os.getenv("PROJECT_ID")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")

def load_schema(schema_path):
    with open(schema_path, 'r') as file:
        return json.load(file)

def generate_prompt(section, data_points):
    prompt = f"Extract the following data points for {section}: {', '.join(data_points)}"
    return prompt

def extract_data(text, schema_path):
    schema = load_schema(schema_path)
    extracted_data = {}

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

    for section, data_points in schema.items():
        prompt = generate_prompt(section, data_points)
        full_prompt = f"{prompt}\n\n{text}"
        generated_response = model.generate(prompt=full_prompt)
        extracted_data[section] = parse_response(generated_response)

    return extracted_data

def parse_response(response):
    generated_text = response.get('results', [{}])[0].get('generated_text', '')
    return generated_text