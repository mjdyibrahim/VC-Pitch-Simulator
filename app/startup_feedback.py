import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SingleStoreDB
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
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

def get_feedback(startup_id, section):
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT raw_text, embedded_text FROM {db_name}.{startup_profile_table}
            WHERE startup_id = :startup_id AND section = :section
        """), {
            "startup_id": startup_id,
            "section": section
        }).fetchone()
    
    if result:
        raw_text, embedded_text = result
        # Perform similarity search
        texts_sim = vectorstore.similarity_search(raw_text, k=5)
        print("Number of relevant texts: " + str(len(texts_sim)))
        print("First 100 characters of relevant texts.")
        for i in range(len(texts_sim)):
            print("Text " + str(i+1) + ": " + str(texts_sim[i].page_content[0:100]))

        # Perform RAG Generation with Explicit Context Control
        chain = load_qa_chain(granite_llm_ibm, chain_type="stuff")
        response = chain.run(input_documents=texts_sim, question=raw_text)
        print("Query: " + raw_text)
        print("Response: " + response)

        # Perform RAG Generation with Q&A Chain
        qa = RetrievalQA.from_chain_type(llm=granite_llm_ibm, chain_type="stuff", retriever=vectorstore.as_retriever())
        response = qa.run(raw_text)
        print("Query: " + raw_text)
        print("Response: " + response)
    else:
        print(f"No data found for startup_id: {startup_id}, section: {section}")

if __name__ == "__main__":
    # Example usage
    get_feedback("startup_123", "team")