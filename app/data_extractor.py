from app.ibm_api import initialize_watsonx_ai
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import fitz  # PyMuPDF
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from sqlalchemy import create_engine, text
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_host = os.getenv("SINGLESTORE_HOST")
db_port = int(os.getenv("SINGLESTORE_PORT"))
db_user = os.getenv("SINGLESTORE_USER")
db_password = os.getenv("SINGLESTORE_PASSWORD")
db_name = os.getenv("SINGLESTOR_DATABASE")
db_url = os.getenv("SINGLESTORE_URL")

singlestore_url = f"singlestoredb://{db_url}"

# Connection string to use Langchain with SingleStoreDB
os.environ["SINGLESTOREDB_URL"] = singlestore_url

knowledge_base_engine = create_engine(singlestore_url)

# Initialize IBM Watson Assistant (Granite LLM)
model = initialize_watsonx_ai()  # Ensure this returns the correct model format

embedding_model = HuggingFaceEmbeddings()

def embed_text(text):
    # Ensure the embedding is a 1D vector
    embedded = embedding_model.embed_documents([text])
    return (
        embedded[0] if isinstance(embedded, list) and len(embedded) == 1 else embedded
    )

def cosine_similarity(vec1, vec2):
    return sklearn_cosine_similarity([vec1], [vec2])[0][0]

def call_llm_for_section(text, criteria, section_name):
    prompt = f"""
    Provided the following Pitch Deck content: {text}

    Please summarize the {section_name} and provide feedback for it based on the given criteria:

    {criteria}
    """
    response = model.generate_text(prompt=[prompt])
    print(f"Response for section {section_name}: {response}")  # Debugging line
    # Adjust the following line based on the actual structure of the response
    return {section_name: response[0]}


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
        extracted_sections[section] = {
            "section_text": section_text,
            "nearest_neighbor": nearest_neighbor_result,
        }
    return extracted_sections
