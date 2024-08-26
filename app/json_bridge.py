import os
import json


granite_llm_ibm = WatsonxLLM(model=model)

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_prompt(section, data_point, prompt_template, extracted_text):
    prompt = prompt_template.format(data_point=data_point)
    return f"Given Pitch Deck Content: {extracted_text}\n\nExtracted data for {section}\n\nExtracting Data point {data_point}: {prompt}"

def extract_data(text, schema_path, prompts_path):
    schema = load_json(schema_path)
    prompts = load_json(prompts_path)
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
        extracted_data[section] = {}
        for data_point in data_points:
            prompt_template = prompts.get(section, {}).get(data_point, "")
            if prompt_template:
                prompt = generate_prompt(section, data_point, prompt_template, text)
                response = granite_llm_ibm(prompt)
                extracted_data[section][data_point] = parse_response(response)
        return extracted_data
                
                
def parse_response(response):
    generated_text = response.get('results', [{}])[0].get('generated_text', '')
    return generated_text