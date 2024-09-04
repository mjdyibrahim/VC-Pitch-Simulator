from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ibm import WatsonxLLM

# from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sqlalchemy import create_engine, text
from langchain_core.runnables import RunnableSequence
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

# Connection string to use Langchain with SingleStoreDB
os.environ["SINGLESTOREDB_URL"] = singlestore_url

knowledge_base_engine = create_engine(singlestore_url)

# Initialize IBM Watson Assistant (Granite LLM)
ibm_api_key = os.getenv("IBM_API_KEY")
ibm_project_id = os.getenv("PROJECT_ID")
ibm_cloud_url = os.getenv("IBM_CLOUD_URL")

print(f"IBM API Key: {ibm_api_key}")
print(f"IBM Project ID: {ibm_project_id}")
print(f"IBM Cloud URL: {ibm_cloud_url}")

if not ibm_api_key or not ibm_project_id or not ibm_cloud_url:
    raise ValueError(
        "IBM Watson credentials are not set properly in the environment variables."
    )

model = Model(
    model_id=ModelTypes.GRANITE_13B_CHAT_V2,
    params={
        GenParams.MAX_NEW_TOKENS: 900,
        GenParams.RETURN_OPTIONS: {
            "input_text": True,
            "generated_tokens": True,
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

def embed_text(text):
    # Ensure the embedding is a 1D vector
    embedded = embedding_model.embed_documents([text])
    return (
        embedded[0] if isinstance(embedded, list) and len(embedded) == 1 else embedded
    )


def cosine_similarity(vec1, vec2):
    return sklearn_cosine_similarity([vec1], [vec2])[0][0]
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


def call_llm_for_section(text, criteria, section_name):
    prompt_template = f"""
    Provided the following Pitch Deck content: {{{{text}}}}

    Please summarize the {{{{section_name}}}} and provide feedback for it based on the given criteria:
    
    {{{{criteria}}}}
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["text", "criteria"]
    )
    chain = RunnableSequence(prompt, granite_llm_ibm)
    response = chain.invoke({"text": text, "criteria": criteria})

    # Return the section name and the extracted information
    return {section_name: response}


def extract_sections(extracted_text, startup_id, content_id):

    sections = {
        "team": [
            """
     Analyze provided content and score the strength of the team section only from 1-10 based on available information and provide feedback on possible improvements.

    Optimal conditions for the team include:
    - 2-3 cofounders, with near equal equity
    - Specialized academic degrees and/or expertise in their areas
    - Half-time or more commitment to the startup
    - Previous startup experience and successful exits
    - Team working together for a significant period
    - Presence of mentors with substantial experience

        Example of team_feedback output format:

        "team_feedback": {
        "feedback_1": "The team has strong experience and a clear vision, but they need more diversity in skills.",
        "feedback_2": "The team's track record is impressive, but they lack experience in scaling businesses.",
        "feedback_3": "There is a strong leadership team, but more emphasis on technical skills is needed.",
        "feedback_4": "The team has a clear vision but needs better execution plans.",
        "feedback_5": "The team should work on improving communication strategies within the group."

    """
        ],
        "fundraising": [
            """
                        Analyze provided content and score the strength of the fundraising section only from 1-10 based on available information and provide feedback on possible improvements.
                        Optimal conditions for fundraising include:
                        - A clear and feasible plan for raising funds in the next 12-18 months
                        - Secured initial funding or demonstrated progress in fundraising
                        - Identified potential sources of funding such as venture capital, angel investors, or grants
                        - Detailed and realistic financial projection
                        - A strong pitch deck and business plan that have been refined and tested with investors

                        Example of fundraising_feedback output format:

                        "fundraising_feedback": {
                        "score": 7,
                        "feedback_1": "The startup has secured initial funding but needs to outline a clearer path for future rounds.",
                        "feedback_2": "Funding sources are diversified, but there is a need for more detailed financial projections.",
                        "feedback_3": "The pitch to investors is strong but needs better risk management strategies.",
                        "feedback_4": "Current funding is sufficient for initial growth but not for scaling.",
                        "feedback_5": "Consider exploring alternative funding options like grants or strategic partnerships."
                        }

                        """
        ],
        "market": [
            """
    Score the strength of the market section from 1-10 based on available information and provide feedback on any possible improvements.
    Optimal conditions for the market include:
    - Clear understanding of the market size and growth potential
    - Defined target market and a plan to capture a significant market share
    - Detailed information on market dynamics, customer needs, and competitive landscape
    - Evidence of market validation, such as customer interviews or pilot studies
    - Strategy for market entry and scaling

    """
        ],
        "business_model": [
            """
    Score the strength of the business model section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for the business model include:
    - Clear revenue model showing how the business will make money
    - Identified who will pay for the service and a strategy for acquiring customers
    - Defined pricing strategy and detailed plan for scaling revenue
    - Identified and planned for key metrics like customer acquisition cost and lifetime value
    - Validated business model with proof of concept or early traction

    """
        ],
        "product": [
            """
    Score the strength of the product section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for the product include:
    - Product is functional and has been tested with users
    - Clear roadmap for product development and future features
    - Feedback from prospective customers indicating strong interest
    - Validated product-market fit or evidence of traction
    - Product solves a significant problem and has unique value propositions
    
    """
        ],
        "traction": [
            """
    Score the strength of the traction section from 1-10 based on available information and provide feedback on possible improvements.
    Optimal conditions for traction include:
    - Demonstrated early sales and revenue growth
    - Clear track record of customer acquisition and retention
    - Metrics and KPIs showing growth and market validation
    - Testimonials or case studies from early customers
    - Clear evidence of traction, such as user growth or partnership agreements


    """
        ],
    }

    # Create the pitchdeck_section table if it doesn't exist
    # create_pitchdeck_section_table()

    def nearest_neighbor_analysis(embedded_text, section_name):
        with knowledge_base_engine.connect() as conn:
            conn.execute(text("USE vc_simulator"))
            result = conn.execute(text("SELECT content FROM knowledge_base"))
            section_contents = [row[0] for row in result]
            section_embeddings = [embed_text(content) for content in section_contents]

            # Perform nearest neighbor analysis using cosine similarity
            similarities = [
                cosine_similarity(embedded_text, embedding)
                for embedding in section_embeddings
            ]
            nearest_neighbor_result = max(similarities) if similarities else None
            return nearest_neighbor_result

    extracted_sections = {}
    for section, criteria in sections.items():
        response = call_llm_for_section(extracted_text, criteria, section)
        section_text = response[section]
        embedded_text = embed_text(section_text)
        extracted_sections[section] = section_text
        nearest_neighbor_result = nearest_neighbor_analysis(embedded_text, section)
        # store_section_data(startup_id, section, response, embedded_text, content_id)
        extracted_sections[section] = {
            "section_text": section_text,
            "nearest_neighbor": nearest_neighbor_result,
        }
    return extracted_sections
