from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
# from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_host = os.getenv("SINGLESTORE_HOST")
db_port = int(os.getenv("SINGLESTORE_PORT"))
db_user = os.getenv("SINGLESTORE_USER")
db_password = os.getenv("SINGLESTORE_PASSWORD")
db_name = os.getenv("SINGLESTORE_DATABASE")
db_url = os.getenv("SINGLESTORE_URL")

singlestore_url = f"singlestoredb://{db_url}"

# engine = create_engine(singlestore_url)

# Initialize IBM Watson Assistant (Granite LLM)
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_project_id = os.getenv("PROJECT_ID")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")

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

granite_llm_ibm = WatsonxLLM(model=model)
embedding_model = HuggingFaceEmbeddings()

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def embed_text(text):
    return embedding_model.embed_text(text)

# def create_pitchdeck_section_table():
    # with engine.connect() as conn:
    #     conn.execute(text(f"""
    #         CREATE TABLE IF NOT EXISTS {db_name}.pitchdeck_section (
    #             id SERIAL PRIMARY KEY,
    #             startup_id VARCHAR(255),
    #             section_name VARCHAR(255),
    #             section_content TEXT,
    #             section_embedding TEXT,
    #             content_id INTEGER,
    #             created_at TIMESTAMP,
    #             updated_at TIMESTAMP,
    #             FOREIGN KEY (content_id) REFERENCES {db_name}.pitchdeck_content(id)
    #         )
    #     """))

# def store_section_data(content_id, section_name, raw_text, embedded_text):
    # with engine.connect() as conn:
    #     conn.execute(text(f"""
    #         INSERT INTO {db_name}.pitchdeck_section (content_id, section_name, section_content, section_embedding, content_id)
    #         VALUES (:startup_id, :section_name, :section_content, :section_embedding, :content_id, :created_at, :updated_at, :content_id)
    #     """), {
    #         "section_name": section_name,
    #         "section_content": raw_text,
    #         "section_embedding": embedded_text,
    #         "content_id": content_id,
    #         "created_at": datetime.utcnow(),
    #         "updated_at": datetime.utcnow(),
    #         "content_id": content_id
    #     })
    #     return 

# def retrieve_sections(startup_id):
#     with engine.connect() as conn:
#         result = conn.execute(text(f"""
#             SELECT section_name, section_content FROM {db_name}.pitchdeck_section
#             WHERE startup_id = :startup_id
#         """), {"startup_id": startup_id})
#         data = {}
#         for row in result:
#             data[row["section_name"]] = row["section_content"]
#     return data

def call_llm_for_section(text, questions, section_name):
    prompt_template = f"""
    Text: {{text}}

    Questions for {section_name}:
    {{questions}}
    """
    questions_str = "\n".join([f"- {question}" for question in questions])
    prompt = PromptTemplate(template=prompt_template, input_variables=["text", "questions"])
    chain = LLMChain(llm=granite_llm_ibm, prompt=prompt)
    response = chain.run({"text": text, "questions": questions_str})
    
    # Return the section name and the extracted information
    return {section_name: response}

def extract_sections(file_path, startup_id, content_id):
    text = extract_text_from_pdf(file_path)
    
    sections = {
        "team": [
            "How many team members do you have?",
            "List the team members with the following details:",
            "What is the team member's name?",
            "What is the team member's title?",
            "How many hours per week is the team member available?",
            "Since when has the team member been involved?",
            "What percentage of equity does the team member hold?",
            "What percentage of salary does the team member receive?",
            "How many years of experience does the team member have?",
            "Does the team member have an undergraduate degree?",
            "Does the team member have a graduate degree?",
            "Does the team member have a master's degree?",
            "Does the team member have a PhD or higher degree?",
            "Has the team member been part of a startup team?",
            "Has the team member been the founder of a startup?",
            "Has the team member held a previous C-level position?",
            "Has the team member been part of a successful exit?",
            "Is the team member's role in Marketing?",
            "Is the team member's role in Sales?",
            "Is the team member's role in Product?",
            "Is the team member's role in Creative?",
            "Is the team member's role in Technical?",
            "Is the team member's role in Operation?",
            "What other role does the team member have?",
            "Can you provide an overview of the team's qualifications and expertise?",
            "How would you assess the team's experience and ability to execute the business plan?"
        ],
        "fundraising": [
            "What is the current stage of fundraising?",
            "What is the target amount of funding?",
            "What is the current amount of funding?",
            "What is the minimum amount of funding?",
            "What is the maximum amount of funding?"
        ],
        "market": [
            "What is the primary industry?",
            "What is the market size?",
            "What is the market share in 3 years?"
        ],
        "business_model": [
            "What is the primary industry?",
            "What is the market size?",
            "What is the market share in 3 years?"
        ],
        "product": [
            "What is the product?",
            "What is the product's unique selling proposition?",
            "What is the product's competitive advantage?"
        ],
        "traction": [
            "What is the traction?",
            "What is the traction's unique selling proposition?",
            "What is the traction's competitive advantage?"
        ]
    }
    
    # Create the pitchdeck_section table if it doesn't exist
    # create_pitchdeck_section_table()

    extracted_sections = {}
    for section, questions in sections.items():
        response = call_llm_for_section(text, questions, section)
        embedded_text = embed_text(response)
        extracted_sections[section] = response
        # store_section_data(startup_id, section, response, embedded_text, content_id)
    return extracted_sections
