import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SingleStoreDB
from langchain.chains import load_qa_chain
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models.extensions.langchain import WatsonxLLM
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings()

# Retrieve database credentials from environment variables
db_url = os.getenv("SINGLESTORE_URL")
db_name = os.getenv("SINGLESTORE_DATABASE")
startup_profile_table = "startup_profile"

# Connection string to use Langchain with SingleStoreDB
os.environ["SINGLESTOREDB_URL"] = f"{db_url}"

# Initialize the vector store
vectorstore = SingleStoreDB(
    embedding=embedding_model,
    table_name="knowledge_base"
)

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

engine = create_engine(f"singlestoredb://{db_url}")

def start_chat_session(startup_id):
    # Example chat session logic
    print("Starting chat session with user...")
    # Ask critical questions and update knowledge base
    # This is a placeholder for actual chat logic
    questions = [
        "What is your team size?",
        "What is your current fundraising status?",
        "What market are you targeting?",
        "What is your business model?",
        "What is your production capacity?",
        "What traction have you achieved so far?"
    ]
    for question in questions:
        response = input(question + " ")
        # Store the response in the database
        with engine.connect() as conn:
            conn.execute(text(f"""
                INSERT INTO {db_name}.{startup_profile_table} (startup_id, section, raw_text)
                VALUES (:startup_id, :section, :raw_text)
            """), {
                "startup_id": startup_id,
                "section": question,
                "raw_text": response
            })
    print("Chat session completed.")

def generate_action_plan(startup_id):
    # Example action plan generation logic
    print("Generating action plan for user...")
    action_plan = "Based on our chat session, here is your action plan:\n"
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT section, raw_text FROM {db_name}.{startup_profile_table}
            WHERE startup_id = :startup_id
        """), {
            "startup_id": startup_id
        })
        for row in result:
            section, raw_text = row
            action_plan += f"{section}: {raw_text}\n"
    print(action_plan)

if __name__ == "__main__":
    # Example usage
    start_chat_session("startup_123")
    generate_action_plan("startup_123")
