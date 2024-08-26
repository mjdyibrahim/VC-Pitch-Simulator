import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import SingleStoreDB
from langchain.docstore.document import Document

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

# Ensure the database is selected before any operation
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.execute(text(f"USE {db_name}"))
    conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
    conn.execute(text(f"CREATE TABLE {table_name} (content LONGTEXT, vector BLOB, metadata JSON)"))
    conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {startup_profile_table} (
            id SERIAL PRIMARY KEY,
            startup_id VARCHAR(255) NOT NULL,
            section VARCHAR(255) NOT NULL,
            raw_text TEXT,
            embedded_text BLOB
        )
    """))
    print("Database and tables created/verified.")

print("Available databases:")
with engine.connect() as conn:
    result = conn.execute(text("SHOW DATABASES"))
    for row in result:
        print(row)

# Connection string to use Langchain with SingleStoreDB
os.environ["SINGLESTOREDB_URL"] = singlestore_url

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
                else:
                    try:
                        loader = TextLoader(file_path, encoding='utf-8')  # Specify encoding
                        docs = loader.load()
                        text = docs[0].page_content  # Assuming single document per file
                    except UnicodeDecodeError:
                        print(f"Error loading {file_path}: UnicodeDecodeError")
                        continue
                
                # Split the text into chunks
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = text_splitter.split_text(text)
                all_texts.extend(chunks)
                metadata_list.extend([{"file_name": file_name}] * len(chunks))

            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    # Convert all_texts to Document format
    documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(all_texts, metadata_list)]

    # Store the documents in SingleStoreDB
    vectorstore = SingleStoreDB.from_documents(
        database="vc_simulator",
        documents=documents,
        embedding=embedding_model,
        table_name=table_name,
    )

    # Describe the schema and count rows in both tables
    with engine.connect() as conn:
        result = conn.execute(text(f"DESCRIBE {table_name}"))
        print(f"{table_name} table schema:")
        for row in result:
            print(row)

        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        print(f"\nNumber of rows in {table_name}: {str(result.first()[0])}")

        result = conn.execute(text(f"DESCRIBE {startup_profile_table}"))
        print(f"{startup_profile_table} table schema:")
        for row in result:
            print(row)

        result = conn.execute(text(f"SELECT COUNT(*) FROM {startup_profile_table}"))
        print(f"\nNumber of rows in {startup_profile_table}: {str(result.first()[0])}")

if __name__ == "__main__":
    load_and_store_documents()
