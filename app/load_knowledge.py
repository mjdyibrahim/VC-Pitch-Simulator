import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import SingleStoreDB
import fitz  # PyMuPDF

# Load environment variables from .env file
load_dotenv()

embedding_model = HuggingFaceEmbeddings()

knowledge_base_dir = "knowledge_base" 

# Retrieve database credentials from environment variables
db_host = os.getenv("SINGLESTORE_HOST")
db_port = int(os.getenv("SINGLESTORE_PORT"))
db_user = os.getenv("SINGLESTORE_USER")
db_password = os.getenv("SINGLESTORE_PASSWORD")
db_name = os.getenv("SINGLESTORE_DATABASE")
db_url = os.getenv("SINGLESTORE_URL")

table_name = "knowledge_base"
startup_profile_table = "startup_profile"

singlestore_url = f"singlestoredb://{db_url}"

engine = create_engine(singlestore_url)

with engine.connect() as conn:
    db_response = conn.execute(text("CREATE DATABASE IF NOT EXISTS " + db_name))
    table_response = conn.execute(text("CREATE TABLE IF NOT EXISTS " + db_name + "." + table_name + " (vector BLOB, metadata JSON)"))
    profile_table_response = conn.execute(text("""
        CREATE TABLE IF NOT EXISTS """ + db_name + "." + startup_profile_table + """ (
            id SERIAL PRIMARY KEY,
            startup_id VARCHAR(255) NOT NULL,
            section VARCHAR(255) NOT NULL,
            raw_text TEXT,
            embedded_text BLOB
        )
    """))
    print(db_response)
    print(table_response)
    print(profile_table_response)
    
print("Available databases:")
with engine.connect() as conn:
    result = conn.execute(text("SHOW DATABASES"))
    for row in result:
        print(row)
        
# Connection string to use Langchain with SingleStoreDB
os.environ["SINGLESTOREDB_URL"] = f"{db_url}"

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def load_and_store_documents():
    all_texts = []
    metadata_list = []
    for file_name in os.listdir(knowledge_base_dir):
        file_path = os.path.join(knowledge_base_dir, file_name)
        if os.path.isfile(file_path):
            try:
                if file_name.lower().endswith('.pdf'):
                    text = extract_text_from_pdf(file_path)
                    docs = [{"page_content": text}]
                else:
                    try:
                        loader = TextLoader(file_path, encoding='utf-8')  # Specify encoding
                        docs = loader.load()
                    except UnicodeDecodeError:
                        print(f"Error loading {file_path}: UnicodeDecodeError")
                        continue
                    docs = [{"page_content": doc["text"]} for doc in docs]  # Convert to expected format
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                texts = text_splitter.split_documents(docs)
                all_texts.extend(texts)
                metadata_list.extend([{"file_name": file_name}] * len(texts))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    vectorstore = SingleStoreDB.from_documents(
            documents=all_texts,
            embedding=embedding_model,
            table_name=table_name,
            metadata=metadata_list
    )

    # Describe the schema and count rows in both tables
    with engine.connect() as conn:
        result = conn.execute(text("DESCRIBE " + db_name + "." + table_name))
        print(db_name + "." + table_name + " table schema:")
        for row in result:
            print(row)

        result = conn.execute(text("SELECT COUNT(vector) FROM " + db_name + "." + table_name))
        print("\nNumber of rows in " + db_name + "." + table_name + ": " + str(result.first()[0]))

        result = conn.execute(text("DESCRIBE " + db_name + "." + startup_profile_table))
        print(db_name + "." + startup_profile_table + " table schema:")
        for row in result:
            print(row)

        result = conn.execute(text("SELECT COUNT(id) FROM " + db_name + "." + startup_profile_table))
        print("\nNumber of rows in " + db_name + "." + startup_profile_table + ": " + str(result.first()[0]))

if __name__ == "__main__":
    load_and_store_documents()